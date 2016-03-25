# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import render_template
from flask import request
from plumbum import local


app = Flask(__name__)

CONST_PRIVATE_KEY_BEGIN = '-----BEGIN RSA PRIVATE KEY-----'
CONST_PRIVATE_KEY_END = '-----END RSA PRIVATE KEY-----'
CONST_CSR_BEGIN = '-----BEGIN CERTIFICATE REQUEST-----'
CONST_CSR_END = '-----END CERTIFICATE REQUEST-----'
CONST_FORM = 'csr-form.html'


@app.route('/csr', methods=['GET', 'POST'])
def csr():
    if request.method == 'POST':
        return generateCsrJson()
    else:
        return showForm(None, False)


def getOrEmpty(dict, var):
    res = ''
    if dict is not None and dict[var] is not None:
        res = dict[var].strip()
    return res


def generateCsrJson():
    csrData = request.get_json()
    commonName = getOrEmpty(csrData, 'commonName')
    if commonName == '':
        return showForm('Domain (Common name) is mandatory!', True)
    else:
        organizationalUnit = getOrEmpty(csrData, 'organizationalUnit')
        organization = getOrEmpty(csrData, 'organization')
        location = getOrEmpty(csrData, 'location')
        state = getOrEmpty(csrData, 'state')
        country = getOrEmpty(csrData, 'country')

        subj = ['/C=', country, '/ST=', state, '/L=', location, '/O=', organization, '/OU=', organizationalUnit, '/CN=', commonName]
        opensslConfPath = '/'.join((app.root_path, 'openssl.conf'))
        openssl = local['openssl']
        result = openssl('req', '-nodes', '-newkey', 'rsa:2048', '-config', opensslConfPath, '-subj', ''.join(subj))

        parsedResult = parseCsr(result)

        if parsedResult is None:
            return showForm('Cannot generate CSR.', True)
        else:
            return jsonify(privateKey=parsedResult[0], csr=parsedResult[1])


def showForm(message, error):
    return render_template(CONST_FORM, message = message, error = error)


def parseCsr(opensslResult):
    if opensslResult != None and opensslResult != '':
        pkBegin = opensslResult.find(CONST_PRIVATE_KEY_BEGIN)
        pkEnd = opensslResult.find(CONST_PRIVATE_KEY_END)
        csrBegin = opensslResult.find(CONST_CSR_BEGIN)
        csrEnd = opensslResult.find(CONST_CSR_END)

        if pkBegin == -1 or pkEnd == -1 or csrBegin == -1 or csrEnd == -1:
            return None
        else:
            pk = opensslResult[pkBegin:pkEnd + len(CONST_PRIVATE_KEY_END)]
            csr = opensslResult[csrBegin:csrEnd + len(CONST_CSR_END)]
            return [pk, csr]
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)