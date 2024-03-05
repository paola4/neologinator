from flask import Flask, request, jsonify, json, render_template
from generator import pages
from generator import pseudoword_generator

def create_app():
    app = Flask(__name__)

    # @app.route('/generate_pseudowords/')
    # def generate_pseudowords():
    #     return pseudoword_generator.get_pseudowords(10, 2)
    
    # TODO: Incorporate the ngram variable
    
    @app.route('/generate_pseudowords', methods= ["GET", "POST"])
    def generate_pseudowords():
        if request.method == 'POST':
            num = request.form.get('num', type=int)
            if num:
                result = pseudoword_generator.get_pseudowords(num, 2)
                return jsonify(result=result)
            else:
                return jsonify(result='Input needed')

        return render_template('result.html')

    app.register_blueprint(pages.bp)
    return app
