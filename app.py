from flask import Flask, request, render_template, redirect, url_for, jsonify
import re

app = Flask(__name__)

lexicon = {
    'python': {
        'keywords': [
            'def', 'return', 'if', 'else', 'for', 'while', 'class', 'import', 'from', 'try', 'except', 'with', 'as', 'assert',
            'break', 'continue', 'pass', 'lambda', 'yield', 'global', 'nonlocal', 'del', 'raise', 'is', 'in', 'and', 'or', 'not', 'None', 'print'
        ],
        'digits': r'\d',
        'identifier': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'variable': r'[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*'
    },
    'javascript': {
        'keywords': [
            'var', 'let', 'const', 'function', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return',
            'try', 'catch', 'finally', 'throw', 'class', 'extends', 'import', 'export', 'new', 'this', 'super', 'null', 'undefined', 'true', 'false', 'console'
        ],
        'digits': r'\d',
        'identifier': r'[a-zA-Z_$][a-zA-Z0-9_$]*',
        'variable': r'[a-zA-Z_$][a-zA-Z0-9_$]*\s*=\s*.*'
    },
    'java': {
        'keywords': [
            'int', 'float', 'double', 'char', 'boolean', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return',
            'try', 'catch', 'finally', 'throw', 'class', 'extends', 'import', 'package', 'new', 'this', 'super', 'null', 'true', 'false', 'System.out.println'
        ],
        'digits': r'\d',
        'identifier': r'[a-zA-Z_$][a-zA-Z0-9_$]*',
        'variable': r'[a-zA-Z_$][a-zA-Z0-9_$]*\s*=\s*.*'
    }
}

def analyze_code(language, code):
    tokens = []
    lang_lexicon = lexicon.get(language)
    
    if not lang_lexicon:
        return {"error": "Language not supported"}
    
    # Tokenize the input code
    for line in code.split('\n'):
        for word in line.split():
            token = {
                'value': word,
                'PR': 'X' if word in lang_lexicon['keywords'] else '',
                'ID': 'X' if re.match(lang_lexicon['identifier'], word) else '',
                'CAD': '',
                'NUM': 'X' if re.match(lang_lexicon['digits'], word) else '',
                'SIMB': '',
                'TIPO': ''
            }
            tokens.append(token)
    
    return tokens

def detect_language(code):
    for language, data in lexicon.items():
        for keyword in data['keywords']:
            if keyword in code:
                return language
    return None

@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code')
    
    if not code:
        return jsonify({"error": "Please provide code"}), 400
    
    language = detect_language(code)
    
    if not language:
        return jsonify({"error": "Could not detect language"}), 400
    
    results = analyze_code(language, code)
    return render_template('index.html', results={language: results}, code=code, language=language)

@app.route('/clear_results', methods=['POST'])
def clear_results():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
