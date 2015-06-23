all:
	./SimpleServer.py

test:
	./markowitz.py

clean:
	-rm gurobi.log *.pyc *.lp
