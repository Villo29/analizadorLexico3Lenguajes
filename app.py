from flask import Flask, request, render_template, redirect, url_for, jsonify
import re

app = Flask(__name__)

lexicon = {
    'python': {
        'keywords': [
            'def', 'return', 'if', 'else', 'for', 'while', 'class', 'import', 'from', 'try', 'except', 'with', 'as', 'assert',
            'break', 'continue', 'pass', 'lambda', 'yield', 'global', 'nonlocal', 'del', 'raise', 'is', 'in', 'and', 'or', 'not', 'None', 'print'
        ],
        'digits': r'\d+',
        'identifier': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'symbols': r'[\[\]{}()=+\-*/%,;.]'
    },
    'javascript': {
        'keywords': [
            'var', 'let', 'const', 'function', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return',
            'try', 'catch', 'finally', 'throw', 'class', 'extends', 'import', 'export', 'new', 'this', 'super', 'null', 'undefined', 'true', 'false', 'console'
        ],
        'digits': r'\d+',
        'identifier': r'[a-zA-Z_$][a-zA-Z0-9_$]*',
        'symbols': r'[\[\]{}()=+\-*/%,;.]'
    },
    'java': {
        'keywords': [
            'int', 'float', 'double', 'char', 'boolean', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return',
            'try', 'catch', 'finally', 'throw', 'class', 'extends', 'import', 'package', 'new', 'this', 'super', 'null', 'true', 'false', 'System.out.println'
        ],
        'digits': r'\d+',
        'identifier': r'[a-zA-Z_$][a-zA-Z0-9_$]*',
        'symbols': r'[\[\]{}()=+\-*/%,;.]'
    }
}

def analyze_code(code):
    tokens = []
    lines = code.split('\n')
    
    for line in lines:
        for word in line.split():
            token = {
                'value': word,
                'PR': '',
                'ID': '',
                'CAD': '',
                'NUM': '',
                'SIMB': '',
                'TIPO': '',
                'python': '',
                'javascript': '',
                'java': '',
                'ERROR': ''
            }
            is_valid = False
            is_symbol = False

            # Check if the token is a keyword, identifier, number, or symbol
            for lang in lexicon:
                if word in lexicon[lang]['keywords']:
                    token['PR'] = 'X'
                    token[lang] = 'X'
                    is_valid = True
                if re.fullmatch(lexicon[lang]['digits'], word):
                    token['NUM'] = 'X'
                    is_valid = True
                if re.fullmatch(lexicon[lang]['identifier'], word):
                    token['ID'] = 'X'
                    is_valid = True
                if re.fullmatch(lexicon[lang]['symbols'], word):
                    token['SIMB'] = 'X'
                    is_valid = True
                    is_symbol = True

            # Determine the type of the token
            if token['PR']:
                token['TIPO'] = 'Palabra Reservada'
            elif token['ID']:
                token['TIPO'] = 'Identificador'
            elif token['NUM']:
                token['TIPO'] = 'Número'
            elif token['SIMB']:
                token['TIPO'] = 'Símbolo'
            else:
                token['ERROR'] = 'X'
                token['TIPO'] = 'Error'
            
            tokens.append(token)
    
    return tokens

@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code')
    
    if not code:
        return jsonify({"error": "Please provide code"}), 400
    
    results = analyze_code(code)
    return render_template('index.html', results=results, code=code)

@app.route('/clear_results', methods=['POST'])
def clear_results():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)