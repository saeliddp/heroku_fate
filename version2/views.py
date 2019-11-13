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
swap = [False, True, True, False, True, True, True, False, False, False, False, False, True, True, False, False, True, False, True, True]
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
        return redirect('version2-instructions')
    else:
        return render(request, 'version2/demographics.html')
    
def instructions(request):
    return render(request, 'version2/instructions.html')

def home(request, id):      
    global left_alg
    global right_alg
    
    if id > 1 and id <= 21:
        # send data to server
        # we will have to have a 'None' algorithm in our database to represent 
        # if the user didn't choose at all
        choice = 'None'
        not_choice = 'None'
        if 'radio' in request.GET:
            if request.GET['radio'] == 'left':
                choice = left_alg
                not_choice = right_alg
            else:
                choice = right_alg
                not_choice = left_alg

        print("User chose: " + choice)
        response = Response(respondent_id=respondent.id,
                            query_id=id-1,
                            chosen_alg_id=Algorithm.objects.filter(name=choice)[0].id,
                            unchosen_alg_id=Algorithm.objects.filter(name=not_choice)[0].id,
                            time_elapsed=int(request.GET['time_elapsed']))
        response.save()
        if id == 11:
            print("switching algos")
            left_alg = round_two_l
            right_alg = round_two_r
            
        if swap[id - 2]:
            temp = left_alg
            left_alg = right_alg
            right_alg = temp
    if id <= 20:
        context = {
            'left_snippets': alg_to_snippets[left_alg][id],
            'right_snippets': alg_to_snippets[right_alg][id],
            'query_name': alg_to_snippets[right_alg][id][0][0],
            'curr_qid': id + 1
        }
        return render(request, 'version2/home.html', context);
    else:
        return redirect('version2-thanks')

def thanks(request):
    return render(request, 'version2/thanks.html')
    
