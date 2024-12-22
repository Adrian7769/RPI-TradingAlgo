# responsible for fetching external data from external sources and storing it in the system on init process

es_bias = None
nq_bias = None 
rty_bias = None
cl_bias = None

def set_bias(es, nq, rty, cl):
    global es_bias, nq_bias, rty_bias, cl_bias
    es_bias = es
    nq_bias = nq
    rty_bias = rty
    cl_bias = cl    
    