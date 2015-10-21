#!/usr/bin/env python

#
#
# Copyright (c) Microsoft Corporation
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
AUTH_TYPES = (("A","Application"),("U","User based"))

class AuthSettings(models.Model):
    user_id = models.ForeignKey(User,related_name="user",unique=True)
    auth_type=models.CharField(max_length=1,default='A',choices=AUTH_TYPES)
    client_id=models.CharField(max_length=1000)
    tenant_id=models.CharField(max_length=1000)
    redirect_uri=models.CharField(max_length=1000)
    client_secret=models.CharField(max_length=1000,blank=True)
    subscription_id=models.CharField(max_length=1000,blank=True)

class AuthSettings_Admin(models.Model):
    user_id=models.CharField(max_length=5,default='Admin',unique=True)
    client_id=models.CharField(max_length=1000)
    tenant_id=models.CharField(max_length=1000)
    redirect_uri=models.CharField(max_length=1000)
    client_secret=models.CharField(max_length=1000,blank=True)
    subscription_id=models.CharField(max_length=1000,blank=True)