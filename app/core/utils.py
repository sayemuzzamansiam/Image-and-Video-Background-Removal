# # app/core/utils.py

# import tempfile

# def write_temp_file(data: bytes, suffix="") -> str:
#     tf = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
#     tf.write(data)
#     tf.flush()
#     tf.close()
#     return tf.name