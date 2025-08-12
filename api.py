from flask import Flask, request, jsonify
from core.seed_generator import argparse, generate_v1_seed, send_local_seed, purge_seed_files
from core.flag_builder import standard, chaos, true_chaos, practice
from core.local_seed_generation import RollException
import os

app = Flask(__name__)

@app.route('/seed', methods=['POST'])
async def create_seed():
    data = request.get_json()
    seed_type = data.get('seed_type', 'standard')
    args = data.get('args', [])

    if seed_type == 'standard':
        flags = await standard()
    elif seed_type == 'chaos':
        flags = await chaos()
    elif seed_type == 'true_chaos':
        flags = await true_chaos()
    elif seed_type == 'practice':
        flags = await practice(data.get('pargs', ''))
    else:
        return jsonify({'error': 'Invalid seed type'}), 400

    try:
        (
            flagstring,
            mtype,
            islocal,
            seed_desc,
            dev,
            filename,
            silly,
            jdm_spoiler,
            localhash,
        ) = await argparse(flags, args, seed_type)

        if islocal:
            zip_path = await send_local_seed(filename, mtype, jdm_spoiler)
            result = {
                'hash': localhash,
                'filename': os.path.basename(zip_path)
            }
            purge_seed_files(filename, "WorldsCollide/seeds/")
        else:
            share_url, seed_hash = await generate_v1_seed(flagstring, seed_desc, dev)
            result = {
                'hash': seed_hash,
                'url': share_url
            }

        return jsonify(result)

    except (RollException, ValueError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
