import time

def gera_codigo_ticket():
    return f"TKT{int(time.time())}"
