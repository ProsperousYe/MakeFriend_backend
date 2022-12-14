#-----------------------------------------------------------#
# -*- coding: utf-8 -*-
# @Time    : 2022/12/15 15:00
# @Author  : Prosperous
# @File    : session.py
# @Software: VSCode
# @Description: this file is about the session between the users
# @Version: 1.0
#-----------------------------------------------------------#
import random
from datetime import datetime
from this import s
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, make_response, send_file, current_app
from flask_mail import Message
from forms import LoginForm, RegisterForm
from flask_restful import Resource, Api
import string
from app import db, mail, socketio
from flask_socketio import emit
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
from models import EmailCaptchaModel, UserModel, SessionModel, MessageModel
from util import verifyEmployeeToken, decodeToken

# 注册了一个bp，名字叫user，前置路径是/user
bp = Blueprint("session", __name__, url_prefix="/api/session")
# 将bp挂载到api上
api = Api(bp)

class SetSession(Resource):
    @verifyEmployeeToken
    def post(self):
        user1_id = request.json.get('user1_id') #user_1是对面的
        user2_id = request.json.get('user2_id') #user_2是自己
        if user1_id is None or user2_id is None or user1_id == "" or user2_id == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        if user1_id == user2_id:
            return jsonify({"error": "Same User",'code': 400})
        if not UserModel.query.filter(UserModel.id==user1_id).first():
            return jsonify({"error": "User1 Not Found",'code': 400})
        if not UserModel.query.filter(UserModel.id==user2_id).first():
            return jsonify({"error": "User2 Not Found",'code': 400})
        current_app.logger.info(str(request.remote_addr)+"][User:"+str(user1_id)+"and User:"+str(user2_id)+" Set Session")
        session = SessionModel.query.filter(or_(and_(SessionModel.user1_id==user1_id, SessionModel.user2_id==user2_id),and_(SessionModel.user1_id==user2_id,SessionModel.user2_id==user1_id))).first()
        if not session:
            session = SessionModel(
                user1_id = user1_id,
                user2_id = user2_id,
            )
            db.session.add(session)
            try:
                db.session.commit()
            except Exception as e:
                return jsonify({"error": "Database Error",'code': 400})
        session_id = session.id
        user1 = UserModel.query.filter(UserModel.id==user1_id).first()
        return jsonify({"code":200,"session_id": session_id, "user1_name": user1.username})

    @verifyEmployeeToken
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Session")
        session_id = request.values.get("session_id")
        if session_id is None or session_id == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        if not SessionModel.query.filter(SessionModel.id==session_id).first():
            return jsonify({"error": "Session Not Found",'code': 400})
        session_ = SessionModel.query.filter(SessionModel.id==session_id).first()
        user_id = request.values.get("user_id")
        print("[get]user_id ",user_id)
        print("[get]session_user1_id ",session_.user1_id)
        if str(user_id) == str(session_.user1_id):
            return jsonify({"code":200,"session_id":session_.id, "user1_id": session_.user2_id, "user2_id":session_.user1_id})
        else:
            return jsonify({"code":200,"session_id":session_.id, "user1_id": session_.user1_id, "user2_id":session_.user2_id})

class Message(Resource):
    @verifyEmployeeToken
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Message")
        session_id = request.values.get("session_id")
        if session_id is None or session_id == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        if not SessionModel.query.filter(SessionModel.id==session_id).first():
            return jsonify({"error": "Session Not Found",'code': 400})
        user_id = decodeToken(request.headers.get("token")).get("id")
        # session = SessionModel.query.filter(SessionModel.id==session_id)
        messages = MessageModel.query.filter(MessageModel.session_id==session_id).order_by(MessageModel.id).all()
        his_messages = []
        for message in messages:
            if(str(message.user_id) != str(user_id)):
                message.state = session_id
                db.session.commit()
            his_messages.append({"filename":message.filename,"id":message.id,"type":message.type,"url":message.url,"content": message.content,"user_id": message.user_id, "year": message.year, "month": message.month, "day": message.day, "hour": message.hour, "minute": message.min, "second": message.sec})
        return jsonify({"code":200,"messages":his_messages})

    @verifyEmployeeToken
    def post(self):
        session_id = request.json.get("session_id")
        if session_id is None or session_id == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        if not SessionModel.query.filter(SessionModel.id==session_id).first():
            return jsonify({"error": "Session Not Found",'code': 400})
        content = request.json.get("content")
        if content is None or content == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        content_ = content.replace(" ", "")
        if content_ is None or content == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        user_id = decodeToken(request.headers.get("token")).get("id")
        dt= datetime.now()
        current_app.logger.info(str(request.remote_addr)+"][User:"+str(user_id)+"Send Message")
        year=dt.year
        month=dt.month
        day=dt.day
        hour=dt.hour
        minute=dt.minute
        second=dt.second
        type = "text"
        state=0
        message = MessageModel(content=content, user_id=user_id, session_id=session_id,
                                year=year, month=month, day=day, hour=hour, min=minute, sec=second,
                                type=type, state=state)
        try:
            db.session.add(message)
            db.session.commit()
            return jsonify({"code":200,"message_id":message.id})
        except Exception as e:
            return jsonify({"error": "Database Error",'code': 400})

    @verifyEmployeeToken
    def delete(self):
        id = request.values.get("message_id")
        if id is None or id == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        message = MessageModel.query.filter(MessageModel.id==id).first()
        if message is None:
            return jsonify({"error": "Message Not Found",'code': 400})
        current_app.logger.warning(str(request.remote_addr)+"][Delete Message:"+str(id)+"")
        try:
            db.session.delete(message)
            db.session.commit()
            return jsonify({"code":200,"message":"Delete Success"})
        except Exception as e:
            return jsonify({"error": "Database Error",'code': 400})

class Upload(Resource):
    @verifyEmployeeToken
    def post(self):
        current_app.logger.info(str(request.remote_addr)+"][Upload ")
        file = request.files.get('file')
        id = request.headers.get('id')
        if file is None or id is None or id == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        filename=file.filename
        filetype=filename.split(".")[-1]
        message = MessageModel.query.filter(MessageModel.id==id).first()
        if message is None:
            return jsonify({"error": "Message Not Found",'code': 400})
        if filetype == "png" or filetype == "jpg" or filetype == "jpeg":
            file.save("asset/chat/files/"+id+"."+filetype)
            type = "image"
            url = "/api/session/upload?filename="+id+"."+filetype
        else:
            file.save("asset/chat/files/"+id+"."+filetype)
            type = "file"
            url = "/api/session/upload_file_content?filename="+id+"."+filetype
        message.type=type
        message.filename=filename
        print("filename",filename)
        message.url=url
        try:
            db.session.commit()
            return jsonify({"code":200,"message":"Upload Success"})
        except Exception as e:
            return jsonify({"error": "Database Error",'code': 400})
    @verifyEmployeeToken
    def get(self):
        filename = request.args.get('filename')
        img_local_path = "./asset/chat/files/" + filename
        try:
            img_f = open(img_local_path, 'rb')
            res = make_response(img_f.read())   # 用flask提供的make_response 方法来自定义自己的response对象
            res.headers['Content-Type'] = 'image/jpg'   # 设置response对象的请求头属性'Content-Type'为图片格式
            img_f.close()
            return res
        except:
            return jsonify({"error": "File Not Found",'code': 400})


class updateFileContent(Resource):
    @verifyEmployeeToken
    def post(self):
        current_app.logger.info(str(request.remote_addr)+"][Upload file content")
        session_id = request.json.get("session_id")
        content = request.json.get("content")
        user_id = decodeToken(request.headers.get("token"))
        if session_id is None or session_id == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        if not SessionModel.query.filter(SessionModel.id==session_id).first():
            return jsonify({"error": "Session Not Found",'code': 400})
        if content is None:
            return jsonify({"error": "Missing Parameter",'code': 400})
        if user_id is None or user_id == "":
            return jsonify({"error": "Missing Parameter",'code': 400})
        user_id = user_id.get("id")
        dt= datetime.now()
        year=dt.year
        month=dt.month
        day=dt.day
        hour=dt.hour
        minute=dt.minute
        second=dt.second
        state=0
        message = MessageModel(content=content, user_id=user_id, session_id=session_id,
                                year=year, month=month, day=day, hour=hour, min=minute, sec=second,
                                state=state)
        try:
            db.session.add(message)
            db.session.commit()
            return jsonify({"id": message.id,"code":200})
        except Exception as e:
            return jsonify({"error": "Database Error",'code': 400})
    @verifyEmployeeToken
    def get(self):
        filename = request.args.get('filename')
        img_local_path = "./asset/chat/files/" + filename
        try:
            return send_file(img_local_path, as_attachment=True, attachment_filename=filename)
        except:
            return jsonify({"error": "File Not Found",'code': 400})


api.add_resource(SetSession, "/session")
api.add_resource(Message, "/message")
api.add_resource(Upload, "/upload")
api.add_resource(updateFileContent, "/update_file_content")
