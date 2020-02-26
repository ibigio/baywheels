import fast_requests as fastr

# Notes:
#
# res_proc should be a function that consumes a
# byte sequence (the body of the response)
# > res_proc: (b'') => ?
#
# middle_res_proc should be a function that
# consumes an HTTP response (and doesn't do
# any operations with the body of it)
# > middle_res_proc: (response) => ?
#
# gen_data should be a list of type DATA
# > gen_data: DATA
#
# req_gen should be a function that consumes type DATA,
# and returns a map (that can be turned into kwargs
# for a request).
# > req_gen: (DATA) => map()

# gen_data = list(range(20000))

# def spitter(d):
# 	params = {'MYARG': d}
# 	headers = {
# 	'api-key':'as9d87f6a9s8d7f6as98df76as9da8ff76fdsasd',
# 	'authorization':'as9d87f6a9s8d7f6as98df76as9da8ffff76'
# 	}
# 	data = {}
# 	data['userLocation'] = {'lat':'1','long':'2'} # TODO: maybe toFloat?
# 	data['qrCode'] = {'memberId':'3', 'qrCode':str(4)}
# 	return {'headers':headers, 'params':params, 'json':data}

# fr.post("https://postman-echo.com/post", reps=10, gen_data=gen_data, req_gen=spitter)
rr = fastr.get('https://postman-echo.com/get', reps=100000)


# def spitter(d):
# 	params = {'MYARG': d}
# 	headers = {
# 	'api-key':'as9d87f6a9s8d7f6as98df76as9da8ff76fdsasd',
# 	'authorization':'as9d87f6a9s8d7f6as98df76as9da8ffff76'
# 	}
# 	data = {}
# 	data['userLocation'] = {'lat':'1','long':'2'} # TODO: maybe toFloat?
# 	data['qrCode'] = {'memberId':'3', 'qrCode':str(4)}
# 	return {'headers':headers, 'params':params, 'json':data}

# r_list = fastr.post('https://postman-echo.com/post', kwargs_list=map(spitter, range(10)))
# print(r_list)

