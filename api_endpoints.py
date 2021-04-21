from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import json


app = Flask(__name__)
api = Api(app)

class Users(Resource):
	def get(self):
		data = pd.read_csv('users.csv')
		data = data.to_dict()

		return {'data': data}, 200

	def post(self):
		parser = reqparse.RequestParser()

		parser.add_argument('userId', required=True)
		parser.add_argument('name', required=True)
		parser.add_argument('city', required=True)

		args = parser.parse_args()

		data = pd.read_csv('users.csv')
		if args['userId'] in list(data['userId']):
			return {
				'message': f"'{args['userId']}' already exists!"
			}, 401
		else:
			new_data = pd.DataFrame({
				'userId': args['userId'],
				'name': args['name'],
				'city': args['city'],
				'location': [[]]
				})			
			data = data.append(new_data, ignore_index=True)
			data.to_csv('users.csv', index=False)

			return {'data': data.to_dict()}, 200

	def put(self):
	        parser = reqparse.RequestParser()  # initialize
	        parser.add_argument('userId', required=True)  # add args
	        parser.add_argument('location', required=True)
	        args = parser.parse_args()  # parse arguments to dictionary

	        # read our CSV
	        data = pd.read_csv('users.csv')
	        
	        if args['userId'] in list(data['userId']):

	            # evaluate strings of lists to lists
	            data['locations'] = data['locations'].astype(str).apply(
	                lambda x: x.strip('][').split(', ')
	            )
	            # select our user
	            user_data = data[data['userId'] == args['userId']]

	            # update user's locations
	            user_data['locations'] = user_data['locations'].values[0] \
	                .append(args['location'])
	            
	            # save back to CSV
	            data.to_csv('users.csv', index=False)
	            # return data and 200 OK
	            return {'data': data.to_dict()}, 200

	        else:
	            # otherwise the userId does not exist
	            return {
	                'message': f"'{args['userId']}' user not found."
	            }, 404

	def delete(self):
		parser = reqparse.RequestParser()
		parser.add_argument('userId')
		args = parser.parse_args()

		data = pd.read_csv('users.csv')

		if args['userId'] in list(data['userId']):
			to_drop = data[data['userId'] == args['userId']].index
			data.drop(to_drop, inplace=True)

			data.to_csv('users.csv', index=False)
			return {
				'data': data.to_dict()
			}, 200
			
		else:
			return {
				'message': "User '{}' not found".format(args['userId'])
			}, 404



class Locations(Resource):
	pass

api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')



if __name__ == '__main__':
	app.run()