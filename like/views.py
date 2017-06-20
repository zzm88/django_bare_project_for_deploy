from django.shortcuts import render
from pinry.core.models import *
from pinry.users.models import User
from django.http import JsonResponse

def like(request,pin_id):
    p = Pin.objects.get(id = pin_id)
    u_id = request.user.id
    # p.votes.delete(u_id) if p.votes.exists(u_id) else p.votes.up(u_id)
    p.votes.up(u_id)
    vote_count = p.votes.count()
    p.save()
    return JsonResponse({'click-success': 1,'vote-count':vote_count})

def unlike(request,pin_id):
    p = Pin.objects.get(id = pin_id)
    u_id = request.user.id
    p.votes.delete(u_id)
    vote_count = p.votes.count()
    p.save()
    return JsonResponse({'click-success': 1,'vote-count':vote_count})

# detect a pin has been voted by request user or not.( seems I didn't use it at all)
def is_voted(request,pin_id):
    p = Pin.objects.get(id = pin_id)
    u_id = request.user.id
    voted = p.votes.exists(u_id)
    return  JsonResponse({'voted':voted})

# been used in like.js-> getVotedPin()
def voted_pins(request):
    voted_pins = Pin.votes.all(request.user.id)
    def get_id(pin_object):
        return pin_object.id
    voted_pins = map(get_id,voted_pins)
    return  JsonResponse({'voted_pins':voted_pins})







#!/usr/bin/env python# Create your views here.
