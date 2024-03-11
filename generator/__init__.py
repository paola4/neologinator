from flask import Flask, request, jsonify, render_template, Response
from generator import pages
from generator import pseudoword_generator

def create_app():
    app = Flask(__name__)

    # TODO: Incorporate the ngram variable
    
    @app.route('/generate_pseudowords', methods= ["GET", "POST"])
    def generate_pseudowords():
        if request.method == 'POST':
            num = request.form.get('num', type=int)
            ngram = request.form.get('ngram', type=int)
            if num and ngram:
                result = pseudoword_generator.get_pseudowords(num, ngram)
                # resp_json = Response(json.dumps(result))
                # return resp_json
                # return jsonify(result=result)
                result_l = []
                for r in result:
                    result_l.append(r[0])
                result = ', '.join(result_l)
                # return render_template('_generate_pseudowords.html', result=result)
                return jsonify(result=result)
            else:
                return jsonify(result='Input needed')

        return render_template('_generate_pseudowords.html')

    app.register_blueprint(pages.bp)
    return app
