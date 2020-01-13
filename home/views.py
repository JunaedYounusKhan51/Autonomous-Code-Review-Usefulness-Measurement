# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from control.models import Menu, Role, User
from .models import Project, Commit, Review

from curl.Classification.Classifier import Classifier
from curl.ReviewExtractor import ReviewExtractor
from curl.Classification.ReviewModifier.ReviewModifier import ReviewModifier
from report.DbQueryProject import DbQueryProject
from collections import Counter

# Create your views here.

def login(request):    
    return render(request,'home/login.html')

def home(request):    
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        
        projects = Project.objects.filter(authors = user)
        context = {
            'menus': menus,
            'projects' : projects,
        }
        return render(request,'home/home.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def upload_code_review(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        
        context = {'menus': menus}
        return render(request,'home/upload_code_review.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))    

def project(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        authors = User.objects.all()        
        context = {
            'menus': menus,
            'authors': authors,            
        }
        return render(request,'home/project.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))    

def project_add(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        
        project = Project(
            name = request.POST['name'],
            url = request.POST['url'],
            description = request.POST['description'],            
            created_by = request.session['userid']        
        )
        project.save()

        project.authors = request.POST.getlist('authors')
        project.save()

                
        reviewExtractor=ReviewExtractor(request.POST['url'])
        reviewExtractor.query(request.POST['name'])        
        
        curl_manage(project, reviewExtractor)

        return HttpResponseRedirect(reverse('project'))
    else:
        return HttpResponseRedirect(reverse('login'))    

def curl_manage(project, reviewExtractor):
    clf = Classifier()
    changeList=reviewExtractor.getChangeList()

    for index,change in enumerate(changeList,start=1):
        commit = Commit(
            project = project,
            commit_id = str(reviewExtractor.getChangeId(change)),
            commit_title = reviewExtractor.getChangeSubject(change)
        )
        commit.save()

        reviewInfo = reviewExtractor.getReviewInfo(change)
        owner=reviewExtractor.getChangeOwner(change)

        for review in reviewInfo:
            reviewer = reviewExtractor.getReviewer(review)
            if ((reviewer.startswith("jenkin")) or reviewer.endswith("jenkin") or (reviewer==owner)):
                continue        

            reviewData = reviewExtractor.getReview(review)
            isLast=reviewExtractor.isLast(change,review)
            clf.feedReview(reviewData,isLast)

            review_db = Review(
                project = project,
                commit = commit,
                review_id = reviewExtractor.getReviewId(review),
                reviewer = reviewer,
                review_time = reviewExtractor.getReviewDate(review),
                review = reviewData,
                usefulness = clf.getPrediction()
            )
            review_db.save()            

def project_list(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        
        projects = Project.objects.all()
        context = {
            'menus': menus,            
            'projects': projects,
        }
        return render(request,'home/project_list.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))    

def project_detail(request, project_id):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        all_author = User.objects.all()        

        this_project = Project.objects.get(pk=project_id)

        authors = []        
        for author in all_author:
            flag = 1
            for x in this_project.authors.all():
                if x.id==author.id:
                    authors.append({'id': author.id, 'userid': author.userid, 'flag': 'selected'})
                    flag = 0
            if flag:
                authors.append({'id': author.id, 'userid': author.userid, 'flag': ''})

        context = {
            'menus': menus,
            'authors': authors,            
            'this_project': this_project,
        }
        return render(request,'home/project_update.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def project_delete(request, project_id):
    if request.session['userid']:        
        this_project = Project.objects.get(pk=project_id)
        Project.objects.get(pk=project_id).delete()
        Review.objects.filter(project=this_project).delete()
        Commit.objects.filter(project=this_project).delete()
        
        return HttpResponseRedirect(reverse('project_list'))
    else:
        return HttpResponseRedirect(reverse('login'))        

def project_update(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        
        project = Project.objects.get(pk=request.POST['project_id'])
        project.name = request.POST['name']
        project.url = request.POST['url']
        project.description = request.POST['description']
        project.authors = request.POST.getlist('authors')
        project.status = request.POST['status']        
        project.modified_by = request.session['userid']
        project.save()

        reviewExtractor=ReviewExtractor(request.POST['url'])
        reviewExtractor.query(request.POST['name'])        
        
        Review.objects.filter(project=project).delete()
        Commit.objects.filter(project=project).delete()
        curl_manage(project, reviewExtractor)

        return HttpResponseRedirect(reverse('project_list'))
    else:
        return HttpResponseRedirect(reverse('login'))

def projects(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        projects = Project.objects.filter(status='A')

        projectss = []
        
        for p in projects:
            num = Commit.objects.filter(project = p).count()
            projectss.append({'name': p.name, 'description': p.description, 'id': p.id, 'commit_number': num})
            print num

        
                
        context = {
            'menus': menus,
            'projects': projects,
            'projectss' : projectss,            
        }
        return render(request,'home/projects.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))    

def project_commits(request, project_id):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        this_project = Project.objects.get(pk=project_id)
        commits = Commit.objects.filter(project=this_project)
        commitss = []

        for c in commits:
            num = Review.objects.filter(commit = c).count()
            commitss.append({'project': c.project, 'commit_id': c.commit_id, 'commit_title': c.commit_title, 'id': c.id, 'review_number': num})
        
        context = {
            'menus': menus,
            'this_project': this_project,
            'commits' : commits,
            'commitss' : commitss,
        }
        return render(request,'home/project_commits.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def project_reviews(request, commit_id):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        this_commit = Commit.objects.get(pk=commit_id)
        reviews = Review.objects.filter(commit=this_commit)
        
        context = {
            'menus': menus,
            'this_commit': this_commit,
            'reviews' : reviews,
        }
        return render(request,'home/project_reviews.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def project_review_detail(request, review_id):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        

        this_review = Review.objects.get(pk=review_id)
        usefulnesss = ['A','B','C']
        
        context = {
            'menus': menus,                    
            'this_review': this_review,
            'usefulnesss': usefulnesss,
        }
        return render(request,'home/review_update.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def project_review_update(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        
        review = Review.objects.get(pk=request.POST['review_id'])
        old_usefulness = review.usefulness
        review.usefulness = request.POST['usefulness']
        review.save()

        review_description = review.review
        new_usefulness = review.usefulness



        context = {
            'menus': menus,
            'review': review_description,
            'new_usefulness': new_usefulness,
            'old_usefulness': old_usefulness,
        }

        project_review_update_append_in_train_data(review_description, new_usefulness)

        return render(request,'home/review_update_done.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def usefulness_update(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        
        review = Review.objects.get(pk=request.POST['review_id'])
        #old_usefulness = review.usefulness
        review.usefulness = request.POST['usefulness']
        review.save()

        review_description = review.review
        new_usefulness = review.usefulness
        #this_commit = review.commit_id
        commit_id = review.commit_id
        #reviews = Review.objects.filter(commit=this_commit)
        
        project_review_update_append_in_train_data(review_description, new_usefulness)



        #context = {
        #    'menus': menus,
        #    'this_commit': this_commit,
        #    'reviews' : reviews,
        #}
        #return render(request,'home/project_reviews.html', context)

        return HttpResponseRedirect(reverse('project_reviews', kwargs={'commit_id':commit_id}))
    else:
        return HttpResponseRedirect(reverse('login'))        



def project_review_update_append_in_train_data(review_description, new_usefulness):
        rm=ReviewModifier(review_description)
        sampleList=rm.getReviewModifier()

        file_read= open("file_write_test.txt","r")
        lastline = file_read.readlines()[-1] 
        features_of_lastline = lastline.split(",")
        next_serial = int(features_of_lastline[0]) + 1
        print next_serial
        file_read.close()
        
        file_write= open("file_write_test.txt","a+")
        #f.writelines("%s\n" % item  for item in sampleList)
        file_write.write("%d," %next_serial)
        for item in sampleList:
            for x in range(0, 9):
                file_write.write("%s," % item[x])
        file_write.write("%s\n" % new_usefulness)  
        file_write.close()      
        #print sampleList


def customize(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        roles = Role.objects.filter(~Q(id=request.session['notcustomrole']))                
        context = {
            'menus': menus,
            'roles': roles,
        }
        return render(request,'home/customize.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def customize_detail(request, role_id):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all() #ai user er view menu
        roles = Role.objects.filter(~Q(id=request.session['notcustomrole'])) # ai user er role bad baki role
        
        all_menu = Menu.objects.all()
        this_role = Role.objects.get(pk=role_id)
        menu_list = []
        
        for menu in all_menu:
            flag = 1
            for x in this_role.menus.all():
                if x.id==menu.id:
                    menu_list.append({'id': menu.id, 'menu_name': menu.menu_name, 'menu_path': menu.menu_path, 'flag': 'selected'})
                    flag = 0
            if flag:
                menu_list.append({'id': menu.id, 'menu_name': menu.menu_name, 'menu_path': menu.menu_path, 'flag': ''})
                       
        context = {
            'menus': menus,
            'roles': roles,
            'menu_list': menu_list,
            'this_role': this_role,            
        }
        return render(request,'home/customize.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))            

def customize_update(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        roles = Role.objects.filter(~Q(id=request.session['notcustomrole']))

        this_role = Role.objects.get(pk=request.POST['role_id'])
        this_role.menus = request.POST.getlist('role_menus')
        this_role.save()

        context = {
            'menus': menus,
            'roles': roles,
        }
        return render(request,'home/customize.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def search(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        
        context = {'menus': menus}
        return render(request,'home/search.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def searchaction(request):
    if request.session['userid']:        
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()   
        projects = Project.objects.filter(name__contains=request.POST['project_name'])     
        context = {
            'menus': menus,
            'projects' : projects,
            'search_text' : request.POST['project_name'],
        }
        return render(request,'home/search_result.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))    

def report(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        
        context = {'menus': menus}
        return render(request,'home/report.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def report_project(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        
        context = {'menus': menus}
        return render(request,'home/report_project.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def report_reviewer(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        
        context = {'menus': menus}
        return render(request,'home/report_project.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def report_year(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()        
        context = {'menus': menus}
        return render(request,'home/report_project.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def report_project_create(request):
    if request.session['userid']:
        user = User.objects.get(userid=request.session['userid'])
        menus = user.role.menus.all()
        project_name = request.POST['project_name']
        number_of_reviewers = request.POST['number_of_reviewers']
        number_of_reviews = request.POST['number_of_reviews']
        queryProject=DbQueryProject()
        queryProject.getProjectResult(project_name, number_of_reviewers, number_of_reviews)        
        report_path = '/static/home/'+project_name+'.png'
        context = {
                'menus': menus,
                'report_path': report_path,

        }
        return render(request,'home/report_project_create.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))                        

def logout(request):    
    request.session['userid'] = ''
    return HttpResponseRedirect(reverse('login'))

def loginaction(request):
    try:
        user = User.objects.get(userid=request.POST['userid'], password=request.POST['password'])  
        request.session['userid'] = user.userid
        request.session['username'] = user.full_name        
        request.session['userrole'] = user.role.role_name
        request.session['notcustomrole'] = user.role.id
        return HttpResponseRedirect(reverse('home'))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('login'))
