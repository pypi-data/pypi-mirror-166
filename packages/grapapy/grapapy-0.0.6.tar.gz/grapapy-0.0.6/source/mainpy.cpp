#include <pybind11/pybind11.h>

namespace py = pybind11;

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#include <iostream>
#include <string>

#include "grapa/GrapaLink.h"
#include "grapa/GrapaValue.h"
#include "grapa/GrapaSystem.h"
#include "grapa/GrapaCompress.h"

#define gGrapaUseWidget false

extern GrapaSystem* gSystem;
extern bool gGrapaWidgetMainThread;

class GrapaMainResponse : public GrapaConsoleResponse
{
public:
    virtual void SendCommand(GrapaScriptExec* vScriptExec, GrapaNames* pNameSpace, const void* sendbuf, u64 sendbuflen)
    {
    };
    virtual void SendPrompt(GrapaScriptExec* vScriptExec, GrapaNames* pNameSpace, const GrapaBYTE& sendbuf)
    {
    };
    virtual void SendEnd(GrapaScriptExec* vScriptExec, GrapaNames* pNameSpace, GrapaRuleEvent* pValue)
    {
    };
};

template <typename... Args>
using overload_cast_ = pybind11::detail::overload_cast_impl<Args...>;

/* https://pybind11.readthedocs.io/en/stable/classes.html
py::class_<Pet>(m, "Pet")
    .def("set", overload_cast_<int>()(&Pet::set), "Set the pet's age")
    .def("set", overload_cast_<const std::string &>()(&Pet::set), "Set the pet's name");
*/

class  GrapaStruct 
{
public:
    GrapaScriptExec mScriptExec;
    GrapaConsoleSend mConsoleSend;
    GrapaMainResponse mConsoleResponse;
    GrapaNames mRuleVariables;
    GrapaStruct() 
	{
		mConsoleSend.mScriptState.vScriptExec = &mScriptExec;
		mScriptExec.vScriptState = &mConsoleSend.mScriptState;
		mConsoleSend.mScriptState.SetNameSpace(&mRuleVariables);
		mRuleVariables.SetResponse(&mConsoleResponse);
		mConsoleSend.Start();
		GrapaCHAR grresult;
		if (gSystem->mGrammar.mLength)
			grresult = mConsoleSend.SendSync(gSystem->mGrammar);
	}
    ~GrapaStruct() 
	{ 
		mConsoleSend.Stop();
	}
	
    std::string eval(std::string cmdstr)
	{
		std::string r;
		if (cmdstr.length())
		{
			GrapaCHAR runStr(cmdstr.c_str(), cmdstr.length());
			GrapaCHAR grresult = mConsoleSend.SendSync(runStr);
			r.assign((char*)grresult.mBytes, grresult.mLength);
		}
		return r; 
	}
	
	py::bytes evalb(std::string cmdstr)
	{
		std::string r;
		if (cmdstr.length())
		{
			GrapaCHAR runStr(cmdstr.c_str(), cmdstr.length());
			GrapaCHAR grresult = mConsoleSend.SendSync(runStr);
			r.assign((char*)grresult.mBytes, grresult.mLength);
		}
		return py::bytes(r);
	}
	
	std::string exec(py::bytes cmdbytes)
	{
		std::string r;
		std::string cmdstr = py::str(cmdbytes);
		if (cmdstr.length())
		{
			GrapaCHAR runStr(cmdstr.c_str(), cmdstr.length());
			GrapaCHAR grresult = mConsoleSend.SendSync(runStr);
			r.assign((char*)grresult.mBytes, grresult.mLength);
		}
		return r; 
	}

	py::bytes execb(py::bytes cmdbytes)
	{
		std::string r;
		std::string cmdstr = py::str(cmdbytes);
		if (cmdstr.length())
		{
			GrapaCHAR runStr(cmdstr.c_str(), cmdstr.length());
			GrapaCHAR grresult = mConsoleSend.SendSync(runStr);
			r.assign((char*)grresult.mBytes, grresult.mLength);
		}
		return py::bytes(r);
	}

};

std::string Grapaeval(std::string cmdstr)
{
	GrapaStruct gs;
	return gs.eval(cmdstr);
}

py::bytes Grapaevalb(std::string cmdstr)
{
	GrapaStruct gs;
	return gs.evalb(cmdstr);
}

std::string Grapaexec(py::bytes cmdbytes)
{
	GrapaStruct gs;
	return gs.exec(cmdbytes);
}

py::bytes Grapaexecb(py::bytes cmdbytes)
{
	GrapaStruct gs;
	return gs.execb(cmdbytes);
}

PYBIND11_MODULE(grapapy, m)
{
	GrapaCHAR inStr, outStr, runStr;
	bool needExit = false, showConsole = false, showWidget = false;
	GrapaCHAR s = GrapaLink::Start(needExit, showConsole, showWidget, inStr, outStr, runStr);
	
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: cmake_example

        .. autosummary::
           :toctree: _generate

           new - create an instance (state maintained between calls)
		   
		   eval - eval a string, return a string
		   evalb - eval a string, return bytes
		   exec - exec bytes, return a string
		   execb - exec bytes, return bytes
		   
    )pbdoc";

	py::class_<GrapaStruct>(m, "new")
		.def(py::init<>())
		.def("eval", &GrapaStruct::eval,"",py::arg("s"))
		.def("evalb", &GrapaStruct::evalb,"",py::arg("s"))
		.def("exec", &GrapaStruct::exec, "", py::arg("b"))
		.def("execb", &GrapaStruct::execb, "", py::arg("b"))
		;

    m.def("eval", &Grapaeval, R"pbdoc(
        Evaluate a Grapa script
    )pbdoc",
		py::arg("s"));

    m.def("evalb", &Grapaevalb, R"pbdoc(
        Evaluate a Grapa script
    )pbdoc",
		py::arg("s"));

    m.def("exec", &Grapaexec, R"pbdoc(
        Evaluate a Grapa script
    )pbdoc",
		py::arg("b"));
	
    m.def("execb", &Grapaexecb, R"pbdoc(
        Evaluate a Grapa script
    )pbdoc",
		py::arg("b"));
	
    m.attr("__version__") = "0.0.6";
	
	// GrapaLink::Stop();
}
