import pymongo
import datetime
import asyncio
import uvloop
from sanic import app
from sanic import Sanic
from sanic.response import json
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import date
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic("Proyecto")

@app.route('/agregarTemperatura', methods=['POST'])
async def agregarTemperatura(request):
	#En esta parte se recaban los datos del arduino 
	try:
		Temp = request.json['Temp']
		NoCo = request.json['NoCo']
		#en esta parte se determina la hora
		#chora = datetime.datetime.now()
		#hora = chora.strftime('%H:%M:%S.%f')
		dt = datetime.datetime.now()
		output = {'Temp' : Temp, 'NoCo' : NoCo, 'fecha': dt.isoformat()}
		#return json(output)
		#object_id = await app.mongo['api']["datosard"].save(doc)
		#return json({'object_id': str(object_id)})
		mongo_connection = AsyncIOMotorClient('localhost', 27017, io_loop=app.loop)['temperatura']
		conexion = mongo_connection.alumno
		insert = await conexion.insert_one(output)
		return json({"R": 200, "inserted_id": str(insert.inserted_id)})
	except Exception as error:
		print(error)
		return json({"R":500, "mensaje": "Error Servidor"})

	except Exception as errorCli:
		print(errorCli)
		return json({"R":400, "mensaje": "Error Servidor"})
#desplegado de info


#obtener los datos de la bd
@app.route('/obtenerTemperatura', methods=['POST'])
async def obtenerTemperatura(request):
	try:
		Tipo = request.json['Tipo']
		NoCo = request.json['NoCo']
		mongo_connection = AsyncIOMotorClient('localhost', 27017, io_loop=app.loop)['temperatura']
		conexion = mongo_connection.alumno
		if Tipo == "Rango":
			FI = request.json['FI']
			FF = request.json['FF']
			#start = datetime.datetime.strptime(FI, '%Y-%m-%d %H:%M:%S')
			#print(start)
			#end = datetime.datetime.strptime(FF, '%Y-%m-%d %H:%M:%S')
			#print(end)
			#CFI = datetime.datetime.fromisoformat(FI)
			#CFF = datetime.datetime.fromisoformat(FF)
			#data = await conexion.find({'fecha':{ "$lt": end, "$gt": start}}).sort('fecha').to_list(20)
			#data = await conexion.find_one({'fecha':{'$gt': CFI}})
			#print(data)
			data = await conexion.find({'fecha':{ "$gt": FI, "$lt": FF}}).to_list(20)
			print(data)
			#data = await conexion.find({ FI: { '$gt': datetime.datetime.fromisoformat(FI)}, FF: { '$lt': datetime.datetime.fromisoformat(FF)}}).to_list(20)
			lista = []
			for x in data:
				print(x)
				x['id'] = str(x['_id'])
				del x['_id']
				lista.append(x)
			return json({"R":200, "D": lista})
		elif Tipo == "Completa":
			data = await conexion.find().to_list(20)
		#db.bios.find( { birth: { $gt: new Date('1940-01-01'), $lt: new Date('1960-01-01') } } )
			lista = []
			for x in data:
				x['id'] = str(x['_id'])
				del x['_id']
				lista.append(x)
			return json({"R":200, "D": lista})
	except Exception as error:
		print(error)
		status=500
		return json({"R":status, "mensaje": "Error Servidor"})

	except Exception as errorCli:
		print(errorCli)
		return json({"R":400, "mensaje": "Error Servidor"})


loop = asyncio.get_event_loop()
app.run(host="0.0.0.0", port=8000, workers=1)
