from flask import render_template, request
from app import app 
import httpx, json, os

GHC     = os.getenv( 'FORKME_GHC', None )
GHS     = os.getenv( 'FORKME_GHS', None )
OWNER   = os.getenv( 'REPO_OWNER', None )
REPO    = os.getenv( 'REPO_TARGET', None )

REQ_SCOPES  = ['repo']

#TODOs
#   Secret Management
#       In-App
#           Plain
#           Obscure
#           Encrypt
#       Off-App
#           Azure KV
#           AWS Secret Mgr
#           Docker Swarm Secret
#           K8s Secret
#       
#   User Features
#       Name the org being forked to, name the new repo, flag to fork default branch only
#

@app.route('/')
def home():
    app.logger.debug('presenting index.html with https://github.com/login/oauth/authorize?client_id={}&scope=repo%20user'.format(GHC))
    return render_template("index.html", GET_PARAMS = "?client_id={}&scope={}".format(GHC, '%20'.join(REQ_SCOPES)))


@app.route('/do-fork-callback-install-oauth')
def doForkCallbackOAuth():
    app.logger.debug('OAuth Callback received {}'.format(request.values))
    try:
        if 'error_description' in request.values:
            app.logger.error("OAuth Callback bad args {}".format(request.values))
            return render_template("failed.html", failure_message = request.values['error_description'])

        session_code = request.values['code']
    except Exception as e:
        app.logger.error("OAuth Callback unknown exception {}".format(e))
        return render_template("failed.html", failure_message = "Unknown callback request parameters")

    app.logger.debug('Using code to get access token')
    try:
        tok_resp = getAccessToken( session_code )

        if 'failure_message' in tok_resp:
            return render_template("failed.html", failure_message = tok_resp['failure_message'])

        tok = "{} {}".format(tok_resp['token_type'], tok_resp['access_token'])

        try:
            return doFork(tok)
        except Exception as e:
            app.logger.error("Unknown doFork exception {}".format(e))
            return render_template("failed.html", failure_message = "Unable to handle Fork creation")
    except Exception as e:
        app.logger.error("Unknown Access Token exception {}".format(e))
        return render_template("failed.html", failure_message = "Unable to handle Access Token retrieval")



def getAccessToken( session_code ):
    #ignoring state, hijacking is "possible"
    data = {    'client_id':        GHC,
                'client_secret':    GHS,
                'code':             session_code    }
    
    header      = { 'Accept': 'application/json' }
    app.logger  .debug('Sending POST to retrieve access token with headers {} and data {}'.format( header, data ))
    serv_resp   = httpx.post( 'https://github.com/login/oauth/access_token', json = data, headers = header )
    app.logger  .debug('Access Token URL responded to OAuth request with headers {}'.format(serv_resp.headers))

    if not serv_resp.is_success:
        app.logger.error("Access Token for session {} request responded with {}".format(session_code, serv_resp.status_code))
        return { 'failure_message': "Request for Access Token Rejected with Code {}".format(serv_resp.status_code) }

    cleaned     = json.loads(serv_resp.read().decode())
    app.logger  .debug('Access Token URL responded to OAuth request with content {}'.format(cleaned))

    if "error" in cleaned:
        app.logger.error("Access Token request for session {} returned error {}".format(cleaned))
        return { 'failure_message': "Request for Access Token failed for {} - {}".format(cleaned['error'], cleaned['error_description']) }

    if 'repo' not in cleaned['scope']:
        app.logger.error("Access Token for session {} returned an invalid scope, required 'repo' but found {}".format(cleaned))
        return { 'failure_message': 'Access Token was retrieved but it did not contain the Repo scope, only {}. Repo scope is required!'.format(cleaned['scope']) }

    return cleaned


def doFork(tok):
    fork_head   = { 'accept': 'application/vnd.github+json', 'Authorization': '{}'.format(tok) }
    #fork_pload  = { 'name': 'beenForked', 'default_branch_only': True }
    fork_pload  = None
    fork_url    = 'https://api.github.com/repos/{}/{}/forks'.format(OWNER, REPO)

    app.logger  .debug('Sending fork request to {} with headers {} and payload {}'.format(fork_url, fork_head, fork_pload))
    #forked      = httpx.post( fork_url, headers = fork_head, json = fork_pload )
    forked      = httpx.post( fork_url, headers = fork_head )
    app.logger  .debug('Fork request returned headers {}'.format(forked.headers))
    if forked.is_success:
        forked_resp = json.loads(forked.read().decode())
        return render_template("success.html", repo_link = forked_resp['html_url'])
    else:
        cleaned = json.loads(forked.read().decode())
        app.logger.error("Failed to fork URL '{}' with headers '{}' and payload '{}'".format(fork_url, fork_head, fork_pload))
        app.logger.error("{} - {}".format(forked.status_code, cleaned))
        return render_template("failed.html", failure_message = "Fork Denied! {}".format(cleaned['message']))
