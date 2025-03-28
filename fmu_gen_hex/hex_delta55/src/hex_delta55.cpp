/*

FMI Interface for FMU generated by FMICodeGenerator.

This file is part of FMICodeGenerator (https://github.com/ghorwin/FMICodeGenerator)

BSD 3-Clause License

Copyright (c) 2018, Andreas Nicolai
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/

#include <cstring>
#include <sstream>

#include "fmi2common/fmi2Functions.h"
#include "fmi2common/fmi2FunctionTypes.h"
#include "hex_delta55.h"

// FMI interface variables

#define FMI_INPUT_T1_in 1
#define FMI_INPUT_T2_in 2
#define FMI_PARA_m1 3
#define FMI_PARA_m2 4
#define FMI_INPUT_mdot1_in 5
#define FMI_INPUT_mdot2_in 6
#define FMI_PARA_cp1 7
#define FMI_PARA_cp2 8
#define FMI_PARA_K 9
#define FMI_OUTPUT_T1_out 10
#define FMI_OUTPUT_T2_out 11
#define FMI_PARA_ncells 12
#define FMI_PARA_Counterflow 13
#define FMI_LOCAL_T1_out0 14
#define FMI_LOCAL_T2_out1 15
#define FMI_LOCAL_T1_out1 16
#define FMI_LOCAL_T2_out2 17
#define FMI_LOCAL_T1_out2 18
#define FMI_LOCAL_T2_out3 19
#define FMI_LOCAL_T1_out3 20
#define FMI_LOCAL_T2_out4 21
#define FMI_LOCAL_T1_out4 22
#define FMI_LOCAL_T2_out5 23
#define FMI_LOCAL_T1_out5 24
#define FMI_LOCAL_T2_out6 25
#define FMI_LOCAL_T1_out6 26
#define FMI_LOCAL_T2_out7 27
#define FMI_LOCAL_T1_out7 28
#define FMI_LOCAL_T2_out8 29
#define FMI_LOCAL_T1_out8 30
#define FMI_LOCAL_T2_out9 31
#define FMI_PARA_T1_ini 32
#define FMI_PARA_T2_ini 33
#define FMI_LOCAL_T2_out0 34 //only for parallel flow


// *** Variables and functions to be implemented in user code. ***

// *** GUID that uniquely identifies this FMU code
const char * const InstanceData::GUID = "{e1ec4199-143a-11ef-ae6b-e8c8295c8d2e}";

// *** Factory function, creates model specific instance of InstanceData-derived class
InstanceData * InstanceData::create() {
	return new hex_delta55; // caller takes ownership
}


hex_delta55::hex_delta55() :
	InstanceData()
{
	// initialize input variables and/or parameters
	m_realVar[FMI_INPUT_T1_in] = 68;
	m_realVar[FMI_INPUT_T2_in] = 91;
	m_realVar[FMI_PARA_m1] = 400;
	m_realVar[FMI_PARA_m2] = 400;
	m_realVar[FMI_INPUT_mdot1_in] = 46;
	m_realVar[FMI_INPUT_mdot2_in] = 56;
	m_realVar[FMI_PARA_cp1] = 4190;
	m_realVar[FMI_PARA_cp2] = 4190;
	m_realVar[FMI_PARA_K] = 100;
	m_integerVar[FMI_PARA_ncells] = 10;
	m_boolVar[FMI_PARA_Counterflow] = 0;
	m_realVar[FMI_PARA_T1_ini] = 68;
	m_realVar[FMI_PARA_T2_ini] = 91;

	// initialize output variables
	 m_realVar[FMI_OUTPUT_T1_out] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_OUTPUT_T2_out] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out0] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out1] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out1] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out2] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out2] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out3] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out3] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out4] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out4] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out5] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out5] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out6] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out6] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out7] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out7] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out8] = m_realVar[FMI_PARA_T2_ini];
	 m_realVar[FMI_LOCAL_T1_out8] = m_realVar[FMI_PARA_T1_ini];
	 m_realVar[FMI_LOCAL_T2_out9] = m_realVar[FMI_PARA_T2_ini];


}


hex_delta55::~hex_delta55() {
}


// create a model instance
void hex_delta55::init() {
	logger(fmi2OK, "progress", "Starting initialization.");

	if (m_modelExchange) {
		// initialize states
		

		// TODO : implement your own initialization code here
	}
	else {
		// initialize states, these are used for our internal time integration
		

		// TODO : implement your own initialization code here
		m_realVar[FMI_OUTPUT_T1_out] = m_realVar[FMI_PARA_T1_ini];
		m_realVar[FMI_OUTPUT_T2_out] = m_realVar[FMI_PARA_T2_ini];
		m_realVar[FMI_LOCAL_T1_out0] = m_realVar[FMI_PARA_T1_ini];  //14
		m_realVar[FMI_LOCAL_T2_out1] = m_realVar[FMI_PARA_T2_ini];  //15
		m_realVar[FMI_LOCAL_T1_out1] = m_realVar[FMI_PARA_T1_ini]; //16
		m_realVar[FMI_LOCAL_T2_out2] = m_realVar[FMI_PARA_T2_ini]; //17
		m_realVar[FMI_LOCAL_T1_out2] = m_realVar[FMI_PARA_T1_ini];  //18
		m_realVar[FMI_LOCAL_T2_out3] = m_realVar[FMI_PARA_T2_ini];  //19
		m_realVar[FMI_LOCAL_T1_out3] = m_realVar[FMI_PARA_T1_ini];  //20
		m_realVar[FMI_LOCAL_T2_out4] = m_realVar[FMI_PARA_T2_ini]; //21
		m_realVar[FMI_LOCAL_T1_out4] = m_realVar[FMI_PARA_T1_ini];  //22
		m_realVar[FMI_LOCAL_T2_out5] = m_realVar[FMI_PARA_T2_ini];  //23
		m_realVar[FMI_LOCAL_T1_out5] = m_realVar[FMI_PARA_T1_ini];
		m_realVar[FMI_LOCAL_T2_out6] = m_realVar[FMI_PARA_T2_ini];
		m_realVar[FMI_LOCAL_T1_out6] = m_realVar[FMI_PARA_T1_ini];
		m_realVar[FMI_LOCAL_T2_out7] = m_realVar[FMI_PARA_T2_ini];
		m_realVar[FMI_LOCAL_T1_out7] = m_realVar[FMI_PARA_T1_ini];
		m_realVar[FMI_LOCAL_T2_out8] = m_realVar[FMI_PARA_T2_ini];
		m_realVar[FMI_LOCAL_T1_out8] = m_realVar[FMI_PARA_T1_ini];
		m_realVar[FMI_LOCAL_T2_out9] = m_realVar[FMI_PARA_T2_ini]; //31

		m_realVar[FMI_LOCAL_T2_out0] = m_realVar[FMI_PARA_T2_ini];
		// initialize integrator for co-simulation
		m_currentTimePoint = 0;
	}

	logger(fmi2OK, "progress", "Initialization complete.");
}


// model exchange: implementation of derivative and output update
void hex_delta55::updateIfModified() {
	if (!m_externalInputVarsModified)
		return;

	// get input variables
	double T1_in = m_realVar[FMI_INPUT_T1_in];
	double T2_in = m_realVar[FMI_INPUT_T2_in];
	double m1 = m_realVar[FMI_PARA_m1];
	double m2 = m_realVar[FMI_PARA_m2];
	double mdot1_in = m_realVar[FMI_INPUT_mdot1_in];
	double mdot2_in = m_realVar[FMI_INPUT_mdot2_in];
	double cp1 = m_realVar[FMI_PARA_cp1];
	double cp2 = m_realVar[FMI_PARA_cp2];
	double K = m_realVar[FMI_PARA_K];
	int ncells = m_integerVar[FMI_PARA_ncells];
	bool Counterflow = m_boolVar[FMI_PARA_Counterflow];
	double T1_out0 = m_realVar[FMI_LOCAL_T1_out0];  //14
	double T2_out1 = m_realVar[FMI_LOCAL_T2_out1];  //15
	double T1_out1 = m_realVar[FMI_LOCAL_T1_out1]; //16
	double T2_out2 = m_realVar[FMI_LOCAL_T2_out2]; //17
	double T1_out2 = m_realVar[FMI_LOCAL_T1_out2];  //18
	double T2_out3 = m_realVar[FMI_LOCAL_T2_out3];  //19
	double T1_out3 = m_realVar[FMI_LOCAL_T1_out3];  //20
	double T2_out4 = m_realVar[FMI_LOCAL_T2_out4]; //21
	double T1_out4 = m_realVar[FMI_LOCAL_T1_out4];  //22
	double T2_out5 = m_realVar[FMI_LOCAL_T2_out5];  //23
	double T1_out5 = m_realVar[FMI_LOCAL_T1_out5];
	double T2_out6 = m_realVar[FMI_LOCAL_T2_out6];
	double T1_out6 = m_realVar[FMI_LOCAL_T1_out6];
	double T2_out7 = m_realVar[FMI_LOCAL_T2_out7];
	double T1_out7 = m_realVar[FMI_LOCAL_T1_out7];
	double T2_out8 = m_realVar[FMI_LOCAL_T2_out8];
	double T1_out8 = m_realVar[FMI_LOCAL_T1_out8];
	double T2_out9 = m_realVar[FMI_LOCAL_T2_out9]; //31 
	//double T1_ini = m_realVar[FMI_PARA_T1_ini];
	//double T2_ini = m_realVar[FMI_PARA_T2_ini];


	// TODO : implement your code here

	// output variables
	m_realVar[FMI_OUTPUT_T1_out] = 0; // TODO : store your results here
	m_realVar[FMI_OUTPUT_T2_out] = 0; // TODO : store your results here


	// reset externalInputVarsModified flag
	m_externalInputVarsModified = false;
}


// Co-simulation: time integration
void hex_delta55::integrateTo(double tCommunicationIntervalEnd) {

	// state of FMU before integration:
	//   m_currentTimePoint = t_IntervalStart;

	// get input variables

	// double K = m_realVar[FMI_PARA_K];
	int ncells = m_integerVar[FMI_PARA_ncells];
	bool Counterflow = m_boolVar[FMI_PARA_Counterflow];
	// double T1_out0 = m_realVar[FMI_LOCAL_T1_out0]; //14
	// double T2_out1 = m_realVar[FMI_LOCAL_T2_out1]; //15
	// double T1_out1 = m_realVar[FMI_LOCAL_T1_out1]; //16
	// double T2_out2 = m_realVar[FMI_LOCAL_T2_out2]; //17
	// double T1_out2 = m_realVar[FMI_LOCAL_T1_out2]; //18
	// double T2_out3 = m_realVar[FMI_LOCAL_T2_out3]; //19
	// double T1_out3 = m_realVar[FMI_LOCAL_T1_out3]; //20
	// double T2_out4 = m_realVar[FMI_LOCAL_T2_out4]; //21
	// double T1_out4 = m_realVar[FMI_LOCAL_T1_out4];
	// double T2_out5 = m_realVar[FMI_LOCAL_T2_out5];
	// double T1_out5 = m_realVar[FMI_LOCAL_T1_out5];
	// double T2_out6 = m_realVar[FMI_LOCAL_T2_out6];
	// double T1_out6 = m_realVar[FMI_LOCAL_T1_out6];
	// double T2_out7 = m_realVar[FMI_LOCAL_T2_out7];
	// double T1_out7 = m_realVar[FMI_LOCAL_T1_out7];
	// double T2_out8 = m_realVar[FMI_LOCAL_T2_out8];
	// double T1_out8 = m_realVar[FMI_LOCAL_T1_out8];
	// double T2_out9 = m_realVar[FMI_LOCAL_T2_out9]; //31
	// double T1_ini = m_realVar[FMI_PARA_T1_ini];
	// double T2_ini = m_realVar[FMI_PARA_T2_ini];

	// double T2_out0 = m_realVar[FMI_LOCAL_T2_out0]; //34
	double K = m_realVar[FMI_PARA_K];
	double T1_in = m_realVar[FMI_INPUT_T1_in];
	double T2_in = m_realVar[FMI_INPUT_T2_in];
	double m1 = m_realVar[FMI_PARA_m1];
	double m2 = m_realVar[FMI_PARA_m2];
	double mdot1_in = m_realVar[FMI_INPUT_mdot1_in];
	double mdot2_in = m_realVar[FMI_INPUT_mdot2_in];
	double cp1 = m_realVar[FMI_PARA_cp1];
	double cp2 = m_realVar[FMI_PARA_cp2];
	double timestep= (tCommunicationIntervalEnd - m_currentTimePoint);
	int ilocal, i_prev_T1out, i_next_T2out, i_prev_T2out;
	double T1_outcell, T2_outcell, T1_incell, T2_incell;
	double T1_out_t;
	double T2_out_t;
	double Q;

	 // : implement your code here
	for (int icell=0;icell<ncells;icell++){
		//CONNECTIONS BETWEEN THE CELLS AND TO THE EXTERNAL INPUT OUTPUTS:
		if(icell>0){
			i_prev_T1out = 2 * icell + 12;
		}
		else {
			i_prev_T1out = FMI_INPUT_T1_in;
		}

		T1_incell = m_realVar[i_prev_T1out];//T1_out of the prev. cell
		
		if (Counterflow){
			if (icell < (ncells - 1)) {
				i_next_T2out = 2 * icell + 15;
			}
			else {
				i_next_T2out = FMI_INPUT_T2_in;
			}
			T2_incell = m_realVar[i_next_T2out];
		}
		else { //Parallelflow
			if (icell == 0) {
				i_prev_T2out = FMI_INPUT_T2_in;
			}
			else if (icell == 1) {
				i_prev_T2out = FMI_LOCAL_T2_out0;
			}
			else {
				i_prev_T2out = 2 * icell + 11;
			}

			T2_incell = m_realVar[i_prev_T2out]; //T2_out of the prev. cell
		}


		if (icell == (ncells - 1)) {
			T1_out_t = m_realVar[FMI_OUTPUT_T1_out];
		}
		else {
			ilocal = 2 * icell + 14;
			T1_out_t = m_realVar[ilocal];
		}
		

		if(Counterflow){
			if (icell == 0) {
				T2_out_t = m_realVar[FMI_OUTPUT_T2_out];
			}
			else {
				ilocal = 2 * icell + 13;
				T2_out_t = m_realVar[ilocal];
			}
		}
		else { //Parallelflow
			if (icell == (ncells - 1)) {
				T2_out_t = m_realVar[FMI_OUTPUT_T2_out];
			}
			else if (icell == 0) {
				T2_out_t = m_realVar[FMI_LOCAL_T2_out0];
			}
			else {
				ilocal = 2 * icell + 13;
				T2_out_t = m_realVar[ilocal];
			}
		}
		//////////////////////////////////////////////////////////////////////

		Q = K * (T1_out_t - T2_out_t);
		T1_outcell = T1_out_t+timestep*((-Q / m1 / cp1) + (T1_incell - T1_out_t) * mdot1_in / m1);
		T2_outcell = T2_out_t + timestep * ((Q / m2 / cp2) + (T2_incell - T2_out_t) * mdot2_in / m2);

		//////WRITE THE COMPUTED outputs to the local and external variables/////////////////////////////
		if(Counterflow){
			if (icell==0){
				m_realVar[FMI_OUTPUT_T2_out] = T2_outcell;
			}
			else {
				ilocal = 2 * icell + 13;
				m_realVar[ilocal] = T2_outcell;
			}
		}
		else { //Parallel flow
			if (icell == (ncells - 1)) {
				m_realVar[FMI_OUTPUT_T2_out] = T2_outcell;
			}
			else if (icell == 0) {
				m_realVar[FMI_LOCAL_T2_out0] = T2_outcell;
			}
			else {
				ilocal = 2 * icell + 13;
				m_realVar[ilocal] = T2_outcell;
			}

		}

		if (icell==(ncells-1)){
			m_realVar[FMI_OUTPUT_T1_out] = T1_outcell;
		}
		else {
			ilocal = 2 * icell + 14;
			m_realVar[ilocal] = T1_outcell;
		}
		
		
	}



	m_currentTimePoint = tCommunicationIntervalEnd;

	// state of FMU after integration:
	//   m_currentTimePoint = tCommunicationIntervalEnd;
}


void hex_delta55::computeFMUStateSize() {
	// store time, states and outputs
	m_fmuStateSize = sizeof(double)*1;
	// we store all cached variables

	// for all 4 maps, we store the size for sanity checks
	m_fmuStateSize += sizeof(int)*4;

	// serialization of the maps: first the valueRef, then the actual value

	m_fmuStateSize += (sizeof(int) + sizeof(double))*m_realVar.size();
	m_fmuStateSize += (sizeof(int) + sizeof(int))*m_integerVar.size();
	m_fmuStateSize += (sizeof(int) + sizeof(int))*m_boolVar.size(); // booleans are stored as int

	// strings are serialized in checkable format: first length, then zero-terminated string
	for (std::map<int, std::string>::const_iterator it = m_stringVar.begin();
		 it != m_stringVar.end(); ++it)
	{
		m_fmuStateSize += sizeof(int) + sizeof(int) + it->second.size() + 1; // add one char for \0
	}


	// other variables: distinguish between ModelExchange and CoSimulation
	if (m_modelExchange) {

		// TODO : store state variables and already computed derivatives

	}
	else {

		// TODO : store integrator state

	}
}


// macro for storing a POD and increasing the pointer to the linear memory array
#define SERIALIZE(type, storageDataPtr, value)\
{\
  *reinterpret_cast<type *>(storageDataPtr) = (value);\
  (storageDataPtr) = reinterpret_cast<char *>(storageDataPtr) + sizeof(type);\
}

// macro for retrieving a POD and increasing the pointer to the linear memory array
#define DESERIALIZE(type, storageDataPtr, value)\
{\
  (value) = *reinterpret_cast<type *>(storageDataPtr);\
  (storageDataPtr) = reinterpret_cast<const char *>(storageDataPtr) + sizeof(type);\
}


template <typename T>
bool deserializeMap(hex_delta55 * obj, const char * & dataPtr, const char * typeID, std::map<int, T> & varMap) {
	// now de-serialize the maps: first the size (for checking), then each key-value pair
	int mapsize;
	DESERIALIZE(const int, dataPtr, mapsize);
	if (mapsize != static_cast<int>(varMap.size())) {
		std::stringstream strm;
		strm << "Bad binary data or invalid/uninitialized model data. "<< typeID << "-Map size mismatch.";
		obj->logger(fmi2Error, "deserialization", strm.str());
		return false;
	}
	for (int i=0; i<mapsize; ++i) {
		int valueRef;
		T val;
		DESERIALIZE(const int, dataPtr, valueRef);
		if (varMap.find(valueRef) == varMap.end()) {
			std::stringstream strm;
			strm << "Bad binary data or invalid/uninitialized model data. "<< typeID << "-Variable with value ref "<< valueRef
				 << " does not exist in "<< typeID << "-variable map.";
			obj->logger(fmi2Error, "deserialization", strm.str());
			return false;
		}
		DESERIALIZE(const T, dataPtr, val);
		varMap[valueRef] = val;
	}
	return true;
}



void hex_delta55::serializeFMUstate(void * FMUstate) {
	char * dataPtr = reinterpret_cast<char*>(FMUstate);
	if (m_modelExchange) {
		SERIALIZE(double, dataPtr, m_tInput);

		// TODO ModelExchange-specific serialization
	}
	else {
		SERIALIZE(double, dataPtr, m_currentTimePoint);

		// TODO CoSimulation-specific serialization
	}

	// write map size for checking
	int mapSize = static_cast<int>(m_realVar.size());
	SERIALIZE(int, dataPtr, mapSize);
	// now serialize all members of the map
	for (std::map<int,double>::const_iterator it = m_realVar.begin(); it != m_realVar.end(); ++it) {
		SERIALIZE(int, dataPtr, it->first);
		SERIALIZE(double, dataPtr, it->second);
	}
	mapSize = static_cast<int>(m_integerVar.size());
	SERIALIZE(int, dataPtr, mapSize);
	for (std::map<int,int>::const_iterator it = m_integerVar.begin(); it != m_integerVar.end(); ++it) {
		SERIALIZE(int, dataPtr, it->first);
		SERIALIZE(int, dataPtr, it->second);
	}
	mapSize = static_cast<int>(m_boolVar.size());
	SERIALIZE(int, dataPtr, mapSize);
	for (std::map<int,int>::const_iterator it = m_boolVar.begin(); it != m_boolVar.end(); ++it) {
		SERIALIZE(int, dataPtr, it->first);
		SERIALIZE(int, dataPtr, it->second);
	}
	mapSize = static_cast<int>(m_stringVar.size());
	SERIALIZE(int, dataPtr, mapSize);
	for (std::map<int, std::string>::const_iterator it = m_stringVar.begin();
		 it != m_stringVar.end(); ++it)
	{
		SERIALIZE(int, dataPtr, it->first);				// map key
		SERIALIZE(int, dataPtr, static_cast<int>(it->second.size()));		// string size
		std::memcpy(dataPtr, it->second.c_str(), it->second.size()+1); // also copy the trailing \0
		dataPtr += it->second.size()+1;
	}
}


bool hex_delta55::deserializeFMUstate(void * FMUstate) {
	const char * dataPtr = reinterpret_cast<const char*>(FMUstate);
	if (m_modelExchange) {
		DESERIALIZE(const double, dataPtr, m_tInput);

		// TODO ModelExchange-specific deserialization
		m_externalInputVarsModified = true;
	}
	else {
		DESERIALIZE(const double, dataPtr, m_currentTimePoint);

		// TODO CoSimulation-specific deserialization
	}

	if (!deserializeMap(this, dataPtr, "real", m_realVar))
		return false;
	if (!deserializeMap(this, dataPtr, "integer", m_integerVar))
		return false;
	if (!deserializeMap(this, dataPtr, "boolean", m_boolVar))
		return false;

	// special handling for deserialization of string map
	int mapsize;
	DESERIALIZE(const int, dataPtr, mapsize);
	if (mapsize != static_cast<int>(m_stringVar.size())) {
		logger(fmi2Error, "deserialization", "Bad binary data or invalid/uninitialized model data. string-variable map size mismatch.");
		return false;
	}
	for (int i=0; i<mapsize; ++i) {
		int valueRef;
		DESERIALIZE(const int, dataPtr, valueRef);
		if (m_stringVar.find(valueRef) == m_stringVar.end()) {
			std::stringstream strm;
			strm << "Bad binary data or invalid/uninitialized model data. string-variable with value ref "<< valueRef
				 << " does not exist in real variable map.";
			logger(fmi2Error, "deserialization", strm.str());
			return false;
		}
		// get length of string
		int strLen;
		DESERIALIZE(const int, dataPtr, strLen);
		// create a string of requested length
		std::string s(static_cast<size_t>(strLen), ' ');
		// copy contents of string
		std::memcpy(&s[0], dataPtr, static_cast<size_t>(strLen)); // do not copy the trailing \0
		dataPtr += strLen;
		// check that next character is a \0
		if (*dataPtr != '\0') {
			std::stringstream strm;
			strm << "Bad binary data. string-variable with value ref "<< valueRef
				 << " does not have a trailing \0.";
			logger(fmi2Error, "deserialization", strm.str());
			return false;
		}
		++dataPtr;
		// replace value in map
		m_stringVar[valueRef] = s;
	}

	return true;
}


