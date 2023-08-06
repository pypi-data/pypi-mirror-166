#pragma once

#include <Python.h>
#include "pythonTools_doc_en.h"

namespace pyxie {
	typedef struct {
		PyObject_HEAD
	} pyxietools_obj;

	PyObject* tools_loadModel(pyxietools_obj* self, PyObject* args, PyObject* kwargs);
	PyObject* tools_loadAnimation(pyxietools_obj* self, PyObject* args, PyObject* kwargs);
	PyObject* tools_loadCollada(pyxietools_obj* self, PyObject* args, PyObject* kwargs);
	PyObject* tools_loadColladaAnimation(pyxietools_obj* self, PyObject* args, PyObject* kwargs);
	PyObject* tools_convertTextureToPlatform(pyxietools_obj* self, PyObject* args);
	PyObject* tools_compressFolder(pyxietools_obj* self, PyObject* args);
	PyObject* tools_isAlpha(pyxietools_obj* self, PyObject* args);
}
