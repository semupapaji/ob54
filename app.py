#Owner : @vaibhavff570
#Join : @vaibhavapix, @vaibhavapisx
import asyncio
import time
import httpx
import json
from collections import defaultdict
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import protobuf modules
try:
    import FreeFire_pb2, main_pb2, AccountPersonalShow_pb2
    from google.protobuf import json_format
    from Crypto.Cipher import AES
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    # For Vercel, we need to ensure these are installed

# ============ CONFIGURATION ============
G = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
F = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# Updated for OB54
RELEASE_VERSION = "OB54"
CLIENT_VERSION = "1.126.1"

REGNS = ["IND", "BR", "US", "SAC", "NA", "SG", "RU", "ID", "TW", "VN", "TH", "ME", "PK", "CIS", "BD", "EUROPE"]

# ============ INITIALIZATION ============
app = Flask(__name__)
CORS(app)
TOKENS = defaultdict(dict)
UID_MEMORY = {}

# ============ ENCRYPTION FUNCTIONS ============
def BmwNoNoBmvYas(d):
    l = AES.block_size - (len(d) % AES.block_size)
    return d + bytes([l] * l)

def BmwNoiNoiBmvYasYas(k, i, d):
    a = AES.new(k, AES.MODE_CBC, i)
    return a.encrypt(BmwNoNoBmvYas(d))

def PoI(b, mt):
    m = mt()
    m.ParseFromString(b)
    return m

# ============ PROTOBUF HELPERS ============
async def QwE(jt, pt):
    json_format.ParseDict(json.loads(jt), pt)
    return pt.SerializeToString()

# ============ AUTHENTICATION ============
def AsD(reg):
    reg = reg.upper()
    if reg == "IND":
        return "uid=5163888594&password=E0C602A732D4DD8A81F6C03D800ACA8FC5926E94F5FB0107E5608F5F5DDE259C"
    elif reg in {"BR", "US", "SAC", "NA"}:
        return "uid=4044223479&password=EB067625F1E2CB705C7561747A46D502480DC5D41497F4C90F3FDBC73B8082ED"
    else:
        return "uid=4108414251&password=E4F9C33BBEB23C0DA0AD7E60F63C8A05D6A878798E3CD32C4E2314C1EEFD4F72"

async def ZxV(acc):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    data = acc + "&response_type=token&client_type=2&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3&client_id=100067"
    async with httpx.AsyncClient(timeout=30.0) as cl:
        res = await cl.post(url, data=data, headers={
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded"
        })
        d = res.json()
        return d.get("access_token", "0"), d.get("open_id", "0")

async def Bmw(reg):
    try:
        acc = AsD(reg)
        token, oid = await ZxV(acc)
        body = json.dumps({
            "open_id": oid, 
            "open_id_type": "4", 
            "login_token": token, 
            "orign_platform_type": "4"
        })
        pb = await QwE(body, FreeFire_pb2.LoginReq())
        enc = BmwNoiNoiBmvYasYas(G, F, pb)
        url = "https://loginbp.ggpolarbear.com/MajorLogin"
        
        async with httpx.AsyncClient(timeout=30.0) as cl:
            res = await cl.post(url, data=enc, headers={
                'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)",
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip",
                'Content-Type': "application/octet-stream",
                'Expect': "100-continue",
                'X-Unity-Version': "2018.4.11f1",
                'X-GA': "v1 1",
                'ReleaseVersion': RELEASE_VERSION,
                'X-FF-Client-Version': CLIENT_VERSION
            })
            
            msg = json.loads(json_format.MessageToJson(PoI(res.content, FreeFire_pb2.LoginRes)))
            TOKENS[reg] = {
                'token': f"Bearer {msg.get('token','0')}",
                'region': msg.get('lockRegion','0'),
                'server': msg.get('serverUrl','0'),
                'expires': time.time() + 25200
            }
            print(f"✅ Token obtained for region: {reg}")
            return True
    except Exception as e:
        print(f"❌ Error getting token for {reg}: {e}")
        return False

async def GaY():
    tasks = [Bmw(reg) for reg in REGNS]
    results = await asyncio.gather(*tasks)
    return results

async def Gsu():
    while True:
        await asyncio.sleep(25200)
        await GaY()

async def RtY(reg):
    info = TOKENS.get(reg)
    if info and time.time() < info['expires']:
        return info['token'], info['region'], info['server']
    await Bmw(reg)
    info = TOKENS[reg]
    return info['token'], info['region'], info['server']

# ============ MAIN API FUNCTION ============
async def LoL(uid, unk, reg, ep):
    try:
        payload = await QwE(json.dumps({'a': uid, 'b': unk}), main_pb2.GetPlayerPersonalShow())
        data_enc = BmwNoiNoiBmvYasYas(G, F, payload)
        token, lock, server = await RtY(reg)
        
        if not token or token == "Bearer 0":
            return None
            
        async with httpx.AsyncClient(timeout=30.0) as cl:
            res = await cl.post(server + ep, data=data_enc, headers={
                'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)",
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip",
                'Content-Type': "application/octet-stream",
                'Expect': "100-continue",
                'Authorization': token,
                'X-Unity-Version': "2018.4.11f1",
                'X-GA': "v1 1",
                'ReleaseVersion': RELEASE_VERSION,
                'X-FF-Client-Version': CLIENT_VERSION
            })
            
            if res.status_code == 200:
                result = json.loads(json_format.MessageToJson(PoI(res.content, AccountPersonalShow_pb2.AccountPersonalShowInfo)))
                return result
            return None
    except Exception as e:
        print(f"❌ Error in LoL: {e}")
        return None

# ============ FLASK ENDPOINTS ============
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'Online',
        'version': RELEASE_VERSION,
        'client_version': CLIENT_VERSION,
        'endpoints': {
            '/info': 'Get player info by UID',
            '/refresh': 'Refresh tokens',
            '/status': 'Server status'
        }
    })

@app.route('/info', methods=['GET'])
def get_player_info():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"error": "Please provide UID parameter"}), 400
    
    # Check memory cache first
    if uid in UID_MEMORY:
        try:
            reg = UID_MEMORY[uid]
            data = asyncio.run(LoL(uid, "7", reg, "/GetPlayerPersonalShow"))
            if data:
                return jsonify(data)
        except Exception as e:
            print(f"Cache error: {e}")
    
    # Try all regions
    for reg in REGNS:
        try:
            print(f"🔍 Trying region {reg} for UID {uid}")
            data = asyncio.run(LoL(uid, "7", reg, "/GetPlayerPersonalShow"))
            if data:
                UID_MEMORY[uid] = reg
                return jsonify(data)
        except Exception as e:
            print(f"❌ Error with region {reg}: {e}")
            continue
    
    return jsonify({"error": "UID not found in any region"}), 404

@app.route('/refresh', methods=['GET', 'POST'])
def refresh_tokens():
    try:
        asyncio.run(GaY())
        return jsonify({
            'message': 'Tokens refreshed for all regions',
            'regions': len(TOKENS)
        })
    except Exception as e:
        return jsonify({'error': f'Refresh failed: {str(e)}'}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'running',
        'version': RELEASE_VERSION,
        'client_version': CLIENT_VERSION,
        'total_regions': len(REGNS),
        'active_tokens': len(TOKENS),
        'cached_uids': len(UID_MEMORY),
        'regions': list(TOKENS.keys())
    })

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    UID_MEMORY.clear()
    return jsonify({'message': 'Cache cleared'})

# ============ VERCEL HANDLER ============
# This is the entry point for Vercel
async def init_tokens():
    try:
        await GaY()
        print("✅ Tokens initialized")
    except Exception as e:
        print(f"⚠️ Token init error: {e}")

# For Vercel serverless environment
try:
    # Try to initialize tokens for Vercel
    asyncio.run(init_tokens())
except RuntimeError:
    # If already running in event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_tokens())

# ============ MAIN ============
if __name__ == '__main__':
    print("🚀 Starting FreeFire API Server (OB54)")
    print(f"📱 Client Version: {CLIENT_VERSION}")
    print(f"📦 Release Version: {RELEASE_VERSION}")
    print(f"🌍 Regions: {len(REGNS)}")
    
    # Initialize tokens
    try:
        asyncio.run(GaY())
        print("✅ Tokens initialized successfully")
    except Exception as e:
        print(f"⚠️ Token initialization error: {e}")
    
    # Start background token refresh
    async def start_background():
        await GaY()
        asyncio.create_task(Gsu())
    
    # For local development
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
