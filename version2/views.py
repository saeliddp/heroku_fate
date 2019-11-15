from django.shortcuts import render
from django.http import HttpResponse
from version2.extraction import *
from django.shortcuts import redirect
from version2.models import *
import random

num_search_results = 5
# algorithms to be initially displayed on the left and right, respectively
left_alg = "0g"
right_alg = "01gfp"
# algorithms to be displayed on left and right after 10 turns
round_one_l = "0g"
round_one_r = "01gfp"
round_two_l = "05gfp"
round_two_r = "09gfp"

# maps algorithm names to lists of snippets
alg_to_snippets = {
    left_alg: extractFromFile(round_one_l + ".txt", num_search_results),
    right_alg: extractFromFile(round_one_r + ".txt", num_search_results),
    round_two_l: extractFromFile(round_two_l + ".txt", num_search_results),
    round_two_r: extractFromFile(round_two_r + ".txt", num_search_results)
}

# whether or not to swap the left and right algorithms on a given turn
swap = [False, True, True, False, True, True, True, False, False, False, False, False, True, True, False, False, True, False, True, True, False]
respondent = None
def get_ip_address(request):
    """ use requestobject to fetch client machine's IP Address """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip
    
def consent(request):
    return render(request, 'version2/consent.html')
    
def demographics(request):
    if 'age' in request.GET:
        global respondent
        ip = get_ip_address(request)
        respondent = Respondent(
            age=request.GET['age'],
            gender=request.GET['gender'],
            education=request.GET['education'],
            ip_addr=ip)
        respondent.save()
        return redirect('version2-instructions', respondent_id=respondent.id)
    else:
        return render(request, 'version2/demographics.html')
    
def instructions(request, respondent_id):
    context = {
        'respondent_id': respondent_id
    }
    return render(request, 'version2/instructions.html', context)

def getAlgs(id):
    if id < 11 and not swap[id-1]:
        left_alg = round_one_l
        right_alg = round_one_r
    elif id < 11:
        left_alg = round_one_r
        right_alg = round_one_l
    elif not swap[id-1]:
        left_alg = round_two_l
        right_alg = round_two_r
    else:
        left_alg = round_two_r
        right_alg = round_two_l
    
    return [left_alg, right_alg]

def home(request, id):      
    global left_alg
    global right_alg
    
    respid = request.GET['respondent_id']
        
    left_alg = getAlgs(id)[0]
    right_alg = getAlgs(id)[1]
        
    if id > 1 and id <= 21:
        # send data to server
        # we will have to have a 'NO_CHOICE' algorithm in our database to represent 
        # if the user didn't choose at all
        prev_left_alg = getAlgs(id-1)[0]
        prev_right_alg = getAlgs(id-1)[1]
        choice = 'NO_CHOICE'
        not_choice = 'NO_CHOICE'
        if 'radio' in request.GET:
            if request.GET['radio'] == 'left':
                choice = prev_left_alg
                not_choice = prev_right_alg
            else:
                choice = prev_right_alg
                not_choice = prev_left_alg

        response = Response(respondent=Respondent.objects.filter(id=respid)[0],
                            query=Query.objects.filter(query_id=id-1)[0],
                            chosen_alg=Algorithm.objects.filter(name=choice)[0],
                            unchosen_alg=Algorithm.objects.filter(name=not_choice)[0],
                            time_elapsed=int(request.GET['time_elapsed']))
        response.save()
        
    if id <= 20:
        context = {
            'left_snippets': alg_to_snippets[left_alg][id],
            'right_snippets': alg_to_snippets[right_alg][id],
            'query_name': alg_to_snippets[right_alg][id][0][0],
            'curr_qid': id + 1,
            'respondent_id': respid
        }
        return render(request, 'version2/home.html', context);
    else:
        return redirect('version2-thanks')

def thanks(request):
    return render(request, 'version2/thanks.html')
    
