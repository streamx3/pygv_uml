all: clean
	./easy_uml.py test.1.txt test.1.dot
	dot -T png -o test.1.png test.1.dot
	./easy_uml.py test.2.txt test.2.dot
	dot -T png -o test.2.png test.2.dot
	./easy_uml.py test.3.txt test.3.dot
	dot -T png -o test.3.png test.3.dot

clean:
	rm -fv *.dot
	rm -fv *.png
