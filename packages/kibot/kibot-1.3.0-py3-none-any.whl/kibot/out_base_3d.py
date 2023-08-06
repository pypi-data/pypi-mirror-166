# -*- coding: utf-8 -*-
# Copyright (c) 2020-2022 Salvador E. Tropea
# Copyright (c) 2020-2022 Instituto Nacional de Tecnología Industrial
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
import os
import re
import requests
import tempfile
from .error import KiPlotConfigurationError
from .misc import W_MISS3D, W_FAILDL
from .gs import (GS)
from .out_base import VariantOptions, BaseOutput
from .kicad.config import KiConf
from .macros import macros, document  # noqa: F401
from . import log

logger = log.get_logger()
DISABLE_TEXT = '_Disabled_by_KiBot'


class Base3DOptions(VariantOptions):
    def __init__(self):
        with document:
            self.no_virtual = False
            """ *Used to exclude 3D models for components with 'virtual' attribute """
            self.download = True
            """ *Downloads missing 3D models from KiCad git. Only applies to models in KISYS3DMOD """
            self.kicad_3d_url = 'https://gitlab.com/kicad/libraries/kicad-packages3D/-/raw/master/'
            """ Base URL for the KiCad 3D models """
        # Temporal dir used to store the downloaded files
        self._tmp_dir = None
        super().__init__()
        self._expand_id = '3D'

    def download_model(self, url, fname):
        """ Download the 3D model from the provided URL """
        logger.debug('Downloading `{}`'.format(url))
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            logger.warning(W_FAILDL+'Failed to download `{}`'.format(url))
            return None
        if self._tmp_dir is None:
            self._tmp_dir = tempfile.mkdtemp()
            logger.debug('Using `{}` as temporal dir for downloaded files'.format(self._tmp_dir))
        dest = os.path.join(self._tmp_dir, fname)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f:
            f.write(r.content)
        return dest

    def undo_3d_models_rename(self):
        """ Restores the file name for any renamed 3D module """
        for m in GS.get_modules():
            # Get the model references
            models = m.Models()
            models_l = []
            while not models.empty():
                models_l.append(models.pop())
            # Fix any changed path
            replaced = self.undo_3d_models_rep.get(m.GetReference())
            for i, m3d in enumerate(models_l):
                if m3d.m_Filename in self.undo_3d_models:
                    m3d.m_Filename = self.undo_3d_models[m3d.m_Filename]
                if replaced:
                    m3d.m_Filename = replaced[i]
            # Push the models back
            for model in models_l:
                models.push_front(model)

    def replace_models(self, models, new_model, c):
        """ Changes the 3D model using a provided model """
        logger.debug('Changing 3D models for '+c.ref)
        # Get the model references
        models_l = []
        while not models.empty():
            models_l.append(models.pop())
        # Check if we have more than one model
        c_models = len(models_l)
        if c_models > 1:
            new_model = new_model.split(',')
            c_replace = len(new_model)
            if c_models != c_replace:
                raise KiPlotConfigurationError('Found {} models in component {}, but {} replacements provided'.
                                               format(c_models, c, c_replace))
        else:
            new_model = [new_model]
        # Change the models
        replaced = []
        for i, m3d in enumerate(models_l):
            replaced.append(m3d.m_Filename)
            m3d.m_Filename = new_model[i]
        self.undo_3d_models_rep[c.ref] = replaced
        # Push the models back
        for model in models_l:
            models.push_front(model)

    def download_models(self):
        """ Check we have the 3D models.
            Inform missing models.
            Try to download the missing models """
        models_replaced = False
        # Load KiCad configuration so we can expand the 3D models path
        KiConf.init(GS.pcb_file)
        # List of models we already downloaded
        downloaded = set()
        self.undo_3d_models = {}
        extra_debug = GS.debug_level > 3
        # Look for all the footprints
        for m in GS.get_modules():
            ref = m.GetReference()
            # Extract the models (the iterator returns copies)
            models = m.Models()
            models_l = []
            while not models.empty():
                models_l.append(models.pop())
            # Look for all the 3D models for this footprint
            for m3d in models_l:
                if m3d.m_Filename.endswith(DISABLE_TEXT):
                    # Skip models we intentionally disabled using a bogus name
                    if extra_debug:
                        logger.debug("- Skipping {} (disabled)".format(m3d.m_Filename))
                    continue
                used_extra = [False]
                full_name = KiConf.expand_env(m3d.m_Filename, used_extra)
                if extra_debug:
                    logger.debug("- Expanded {} -> {}".format(m3d.m_Filename, full_name))
                if not os.path.isfile(full_name):
                    # Missing 3D model
                    if self.download and (m3d.m_Filename.startswith('${KISYS3DMOD}/') or
                                          m3d.m_Filename.startswith('${KICAD6_3DMODEL_DIR}/')):
                        # This is a model from KiCad, try to download it
                        fname = m3d.m_Filename[m3d.m_Filename.find('/')+1:]
                        replace = None
                        if full_name in downloaded:
                            # Already downloaded
                            replace = os.path.join(self._tmp_dir, fname)
                        else:
                            # Download the model
                            url = self.kicad_3d_url+fname
                            replace = self.download_model(url, fname)
                            if replace:
                                # Successfully downloaded
                                downloaded.add(full_name)
                                self.undo_3d_models[replace] = m3d.m_Filename
                                # If this is a .wrl also download the .step
                                if url.endswith('.wrl'):
                                    url = url[:-4]+'.step'
                                    fname = fname[:-4]+'.step'
                                    self.download_model(url, fname)
                        if replace:
                            m3d.m_Filename = replace
                            models_replaced = True
                    if full_name not in downloaded:
                        logger.warning(W_MISS3D+'Missing 3D model for {}: `{}`'.format(ref, full_name))
                else:  # File was found
                    if used_extra[0]:
                        # The file is there, but we got it expanding a user defined text
                        # This is completely valid for KiCad, but kicad2step doesn't support it
                        m3d.m_Filename = full_name
                        if not models_replaced and extra_debug:
                            logger.debug('- Modifying models with text vars')
                        models_replaced = True
            # Push the models back
            for model in models_l:
                models.push_front(model)
        return models_replaced

    def list_models(self):
        """ Get the list of 3D models """
        # Load KiCad configuration so we can expand the 3D models path
        KiConf.init(GS.pcb_file)
        models = set()
        # Look for all the footprints
        for m in GS.get_modules():
            # Look for all the 3D models for this footprint
            for m3d in m.Models():
                full_name = KiConf.expand_env(m3d.m_Filename)
                if os.path.isfile(full_name):
                    models.add(full_name)
        return list(models)

    def apply_list_of_models(self, enable, slots, m, var):
        # Disable the unused models adding bogus text to the end
        slots = [int(v) for v in slots if v]
        models = m.Models()
        m_objs = []
        # Extract the models, we get a copy
        while not models.empty():
            m_objs.insert(0, models.pop())
        for i, m3d in enumerate(m_objs):
            if self.extra_debug:
                logger.debug('- {} {} {} {}'.format(var, i+1, i+1 in slots, m3d.m_Filename))
            if i+1 not in slots:
                if enable:
                    # Revert the added text
                    m3d.m_Filename = m3d.m_Filename[:-self.len_disable]
                else:
                    # Not used, add text to make their name invalid
                    m3d.m_Filename += DISABLE_TEXT
            # Push it back to the module
            models.push_back(m3d)

    def apply_variant_aspect(self, enable=False):
        """ Disable/Enable the 3D models that aren't for this variant.
            This mechanism uses the MTEXT attributes. """
        # The magic text is %variant:slot1,slot2...%
        field_regex = re.compile(r'\%([^:]+):([\d,]*)\%')     # Generic (by name)
        field_regex_sp = re.compile(r'\$([^:]*):([\d,]*)\$')  # Variant specific
        self.extra_debug = extra_debug = GS.debug_level > 3
        if extra_debug:
            logger.debug("{} 3D models that aren't for this variant".format('Enable' if enable else 'Disable'))
        self.len_disable = len(DISABLE_TEXT)
        variant_name = self.variant.name
        for m in GS.get_modules():
            if extra_debug:
                logger.debug("Processing module " + m.GetReference())
            default = None
            matched = False
            # Look for text objects
            for gi in m.GraphicalItems():
                if gi.GetClass() == 'MTEXT':
                    # Check if the text matches the magic style
                    text = gi.GetText().strip()
                    match = field_regex.match(text)
                    if match:
                        # Check if this is for the current variant
                        var = match.group(1)
                        slots = match.group(2).split(',') if match.group(2) else []
                        # Do the match
                        if var == '_default_':
                            default = slots
                            if self.extra_debug:
                                logger.debug('- Found defaults: {}'.format(slots))
                        else:
                            matched = var == variant_name
                        if matched:
                            self.apply_list_of_models(enable, slots, m, var)
                            break
                    else:
                        # Try with the variant specific pattern
                        match = field_regex_sp.match(text)
                        if match:
                            var = match.group(1)
                            slots = match.group(2).split(',') if match.group(2) else []
                            # Do the match
                            matched = self.variant.matches_variant(var)
                            if matched:
                                self.apply_list_of_models(enable, slots, m, var)
                                break
            if not matched and default is not None:
                self.apply_list_of_models(enable, slots, m, '_default_')

    def filter_components(self):
        self.undo_3d_models_rep = {}
        if not self._comps:
            # No variant/filter to apply
            if self.download_models():
                # Some missing components found and we downloaded them
                # Save the fixed board
                ret = self.save_tmp_board()
                # Undo the changes
                self.undo_3d_models_rename()
                return ret
            return GS.pcb_file
        comps_hash = self.get_refs_hash()
        # Disable the models that aren't for this variant
        self.apply_variant_aspect()
        # Remove the 3D models for not fitted components
        rem_models = []
        for m in GS.get_modules():
            ref = m.GetReference()
            c = comps_hash.get(ref, None)
            if c:
                # The filter/variant knows about this component
                models = m.Models()
                if c.included and not c.fitted:
                    # Not fitted, remove the 3D model
                    rem_m_models = []
                    while not models.empty():
                        rem_m_models.append(models.pop())
                    rem_models.append(rem_m_models)
                else:
                    # Fitted
                    new_model = c.get_field_value(GS.global_field_3D_model)
                    if new_model:
                        # We will change the 3D model
                        self.replace_models(models, new_model, c)
        self.download_models()
        fname = self.save_tmp_board()
        self.undo_3d_models_rename()
        # Undo the removing
        for m in GS.get_modules():
            ref = m.GetReference()
            c = comps_hash.get(ref, None)
            if c and c.included and not c.fitted:
                models = m.Models()
                restore = rem_models.pop(0)
                for model in restore:
                    models.push_front(model)
        # Re-enable the modules that aren't for this variant
        self.apply_variant_aspect(enable=True)
        return fname

    def get_targets(self, out_dir):
        return [self._parent.expand_filename(out_dir, self.output)]


class Base3D(BaseOutput):
    def __init__(self):
        super().__init__()

    def get_dependencies(self):
        files = super().get_dependencies()
        files.extend(self.options.list_models())
        return files
