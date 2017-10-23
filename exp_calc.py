import operator
import math
from re import sub
#from functools import reduce

menu = "+----------------------------------------------------------------------+\n| Tabela de operadores:\n| +     -> Soma\n| -     -> Subtração\n| *     -> Multiplicação\n| /     -> Divisão\n| %     -> Mod\n| ^     -> Exponênciação\n| !     -> Fatorial\n| #     -> Modulo\n| log   -> LogBase (X)\n| sin|h -> Seno / Seno Hiperbólico\n| cos|h -> Cosseno / Cosseno Hiperbólico\n| tan|h -> Tangente / Tangente Hiperbólica\n| deg   -> Converte de RADIANOS para GRAUS\n| rad   -> Converte de GRAUS para RADIANOS\n| e     -> Constante e\n| pi    -> Constante pi\n| =     -> Teste de Igualdade\n| <     -> Menor Que\n| >     -> Maior Que\n|\n| menu  -> Mostra Menu"

def calculate(string):
	ops, stack = {
		"e": math.e,
		"pi": math.pi,
    	"+": operator.add,				#lambda x, y : x + y,
		"-": operator.sub,				#lambda x, y: x - y,
		"*": operator.mul,				#lambda x, y: x * y,
		"/": operator.truediv,			#lambda x, y: x / y,
		"^": operator.pow,				#lambda x, y: x**y,
		"=": operator.eq,				#lambda x, y: x == y,
		"<": operator.lt,				#lambda x, y: x < y,
		">": operator.gt,				#lambda x, y: x > y,
		"%": operator.mod,				#lambda x, y: x % y,
		"#": operator.abs,				#lambda x: +x,
		"~": operator.neg,				#lambda x: -x,
		"!": lambda x: float(math.factorial(x)), 
		#lambda x: reduce((lambda x, y: x * y), [float(n) if n else 1.0 for n in range(0, int(x)+1)]),
		"rad": lambda x: math.radians(x),
		"deg": lambda x: math.degrees(x),
		"log": lambda x, y: math.log(y, x), # is inverted to use same block as normal operations
		"cos": lambda x: math.cos(x),
		"sin": lambda x: math.sin(x),
		"tan": lambda x: math.tan(x),
		"cosh": lambda x: math.cosh(x),
		"sinh": lambda x: math.sinh(x),
		"tanh": lambda x: math.tanh(x),
	}, [] #etc. Just put your operator in here
	if not string: return 0
	for i in string:
		try:
			if i in ["e", "pi"]:
				stack.append(float(ops[i]))
				continue
			stack.append(float(i))
		except ValueError:
			if stack:
				last = float(stack.pop())
				try:
					if i in ["#", "~", "!", "sin", "cos", "tan", "sinh", "cosh", "tanh", "rad", "deg"]:
						try: 
							stack.append(ops[i](last))
						except ValueError:
							stack.append("{} não aceita número negativos/floats.".format(i))
					else:
						try:
							stack.append(ops[i](float(stack.pop()), last))
						except ValueError:
							stack.append("{} não aceita números negativos.".format(i))
						except IndexError:
							stack.append("Falta operandos para {}.".format(i))
				except ZeroDivisionError:
					pass
	if not stack:
		return "Equação não computavel."
	return stack[-1]

def parser(string):
	string = sub(r'([-()+*/^=<>%#~!])(?=)', r' \1 ', string)
	string = sub(r'(log|sinh?|cosh?|tanh?|pi|e|rad|deg|menu)(?=)', r' \1 ', string)
	ops = {
		"+": {"prec" : 2, "assoc": 'L'},
		"-": {"prec" : 2, "assoc": 'L'},
		"*": {"prec" : 3, "assoc": 'L'},
		"/": {"prec" : 3, "assoc": 'L'},
		"(": {"prec" : 9, "assoc": 'L'},
		")": {"prec" : 0, "assoc": 'L'},
		"=": {"prec" : 1, "assoc": 'L'},
		"<": {"prec" : 1, "assoc": 'L'},
		">": {"prec" : 1, "assoc": 'L'},
		"^": {"prec" : 4, "assoc": "R"},
		"!": {"prec" : 4, "assoc": 'R'},
		"%": {"prec" : 3, "assoc": 'L'},
		"#": {"prec" : 4, "assoc": "R"},
		"~": {"prec" : 5, "assoc": "R"},
		"rad": {"prec" : 4, "assoc": 'R'},
		"deg": {"prec" : 4, "assoc": 'R'},
		"log": {"prec" : 7, "assoc": "L"},
		"cos": {"prec" : 6, "assoc": "L"},
		"sin": {"prec" : 6, "assoc": "L"},
		"tan": {"prec" : 6, "assoc": "L"},
		"cosh": {"prec" : 6, "assoc": "L"},
		"sinh": {"prec" : 6, "assoc": "L"},
		"tanh": {"prec" : 6, "assoc": "L"},
	}
	if "menu" in string:
		print(menu)
		return "Menu", 2
	stack, output = [], []
	for i in string.split():
		if i.isalpha() and (i not in ["log", "e", "cos", "sin", "tan", "cosh", "sinh","tanh","pi","rad","deg"]):
			continue
		try:
			if i in ["e", "pi"]:
				output.append(i)
				continue
			float(i)
			output.append(i)
		except ValueError:
			while stack:
				last = stack[-1]
				if (ops[i]["assoc"] == "L" and ops[i]["prec"] <= ops[last]["prec"]) or (ops[i]["assoc"] == "R" and ops[i]["prec"] < ops[last]["prec"]):
					if i != ")":
						if last != "(":
							output.append(stack.pop())
						else:
							break
					else:
						if last != "(":
							output.append(stack.pop())
						else:
							stack.pop()
							break
				else:
					break
			if i != ")":
				stack.append(i)
	while stack:
		output.append(stack.pop())
	if output:
		return output, 0
	return "Não foi possível dar parse na equação.", 1


def reverse(string):
	rvr_str = []
	for i in reversed(string.split()):
		if i == "(":
			rvr_str.append(")")
		elif i == ")":
			rvr_str.append("(")
		else:
			rvr_str.append(i)
	return ' '.join(rvr_str)

print(menu)

while 1:
	x = input("+----------------------------------------------------------------------+\n| Entre com uma expressão matemática: ")
	
	#print("|\n| Equação pós padding: {}".format(x))
	eq, status = parser(x)
	if status:
		print("|\n| Equação pós parsing (Postfix): {}".format(eq))
	else:
		print("|\n| Equação pós parsing (Postfix): {}".format(' '.join(eq)))
	
	#print("|\n| Reverse: {}".format(reverse(x)))
	#eq_pre, status_pre = parser(reverse(x))
	#if status_pre:
	#	print("|\n| Equação pós parsing (Prefix): {}".format(eq))
	#else:
	#	print("|\n| Equação pós parsing (Prefix): {}".format(' '.join(eq_pre[::-1])))
	
	#print("Resposta: {}".format(calc.calc_post(calc.parser(x)[0])))
	
	if status == 1:
		resp = eq
	elif status == 0:
		resp = calculate(eq)
		print("|\n| Resposta: {}\n+----------------------------------------------------------------------+\n".format(resp))
		