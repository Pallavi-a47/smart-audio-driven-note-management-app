import os, time
def logout():
logout_user()
return redirect(url_for('login'))


@app.route('/choose_category')
@login_required
def choose_category():
return render_template('choose_category.html', user=current_user)


@app.route('/speech')
@login_required
def speech():
return render_template('speech.html', user=current_user)


@app.route('/history')
@login_required
def history():
return render_template('history.html', user=current_user)


@app.route('/api/upload', methods=['POST'])
@login_required
def upload_note():
if 'audio' not in request.files:
return jsonify({'error': 'No audio file provided'}), 400
audio = request.files['audio']
category = request.form.get('category', 'uncategorized')
filename = secure_filename(audio.filename)
name, ext = os.path.splitext(filename)
filename = f"{name}_{int(time.time())}{ext}"
filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
audio.save(filepath)


note = VoiceNote(filename=filename, category=category, user_id=current_user.id)
db.session.add(note)
db.session.commit()
return jsonify({'success': True})


@app.route('/api/notes')
@login_required
def list_notes():
notes = VoiceNote.query.filter_by(user_id=current_user.id).order_by(VoiceNote.created_at.desc()).all()
return jsonify([{'id': n.id, 'filename': n.filename, 'category': n.category, 'created_at': n.created_at.isoformat()} for n in notes])


@app.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/delete/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
note = VoiceNote.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
filepath = os.path.join(app.config['UPLOAD_FOLDER'], note.filename)
if os.path.exists(filepath):
os.remove(filepath)
db.session.delete(note)
db.session.commit()
return jsonify({'success': True})


if __name__ == '__main__':
app.run(debug=True)