import sys, os
import re
import datetime,time

import traceback,warnings
from pprint import pprint
import time
from bs4 import BeautifulSoup
import pickle

sys.path.append('.')
import googleapps


def main():
    
    previsit_root_folder = googleapps.drive.Folder('0B1p_s24uqEudNHlZaHUxbm9ZaVU')
    visit_root_folder = googleapps.drive.Folder('0B1p_s24uqEudXzBWUEJtQVl2OUE')
    for netfolder in previsit_root_folder.listfolder(folders_only=True):
        previsit_files = netfolder.listfolder(files_only=True)
        
        visit_folder = googleapps.drive.find(name=netfolder.name, in_folder=visit_root_folder)
        visit_files = visit_folder.listfolder(files_only=True)
        
        print("\nFor " + netfolder.name)
        print("\tPrevisit Files\n\t" + ", ".join(previsit_files))
        print("\tVisit Files\n\t" + ", ".join(visit_files))


def for_principals(slp):

    # get the drive folder
    pm = GoogleDrive.Sheets.SpreadSheet(slp.sheet_service, PROGRESS_MONTORING_SHEET_ID, load_grid=True)

    mailqueue = KMail()
    COUNT =0
    #    mailqueue = GoogleDrive.Sheets.SpreadSheet(slp.sheet_service, MAILER).get_sheet('Mail Queue')
    school_mailer = {}
    with open("OHMYGOD.pckl", 'rb') as fh:
        everything = pickle.load(fh)
        for sid, ref in everything.items():
            if 'slp_school_name' not in ref:
                continue
            if ref['slp_school_name'] in school_mailer:
                raise Exception(":(")
            school_mailer[ ref['slp_school_name'] ] = ref
    
    for network in pm.sheets:

        if network == 'Sheet1':
            continue
        
        sheet = pm.sheets[network]
        matrix = sheet.grid_matrixb()
        for school in matrix.hashmap_matrix():

            if school['form_id'] not in FILTER_PREVISIT_FORMS:
                continue
            
            if school['peso_visit_completed'] == 'Yes' or school['principal_completed_responses'] == 'Yes':
                # all set. Thank you for your service
                print('..completed!')
                continue

            STATUS = None
            print(network + "  -  " + school['school_name'] + "    ", end="")

            if school['principal_completed_responses'] and school['principal_completed_responses'] != 'No':
                # we only expect this cell to be yes or no
                raise Exception(" Don't understand principal completed resposnes value for " + school['principal_completed_responses'])
            elif school['principal_completed_responses'] == 'No':
                # pre-visit form is ready for them, but they didn't do it
                STATUS='AFTERSELECT'
                print(" ---> next step: complete previsit")
            elif school['principal_selected_goals'] == 'Yes':
                raise Exception("how can this be? Why isn't completed resposnes?")
            elif school['principal_selected_goals'] == "Didn't select 3":
                STATUS='RESELECT'
                print(" ---> next step: complete previsit")
            elif not school['principal_selected_goals'] and not school['principal_completed_responses']:
                # they didnt do anything
                STATUS='BEGIN'
                print(" ---> next step: begin")
            else:
                raise Exception("???")

            queue_email(mailqueue, STATUS, school_mailer[school['school_name']], SA[network.strip()], school)
            time.sleep(1)
            
def queue_email(mailqueue,status, ref, senior_associate, schoolprogress):
    
    p = ref['email']['sy2017-2018_principal'].splitlines()
    if p[0] == 'Sharon Marino':
        p = [p[0] + ' and ' + p[1]]
        e = [ref['email']['email'].strip()]
    else:
        e = ref['email']['email'].splitlines()

    principals = ' and '.join(p)
    emails = ', '.join('"' +p[i].strip() + '"' + '<' + e[i].strip() + '>' for i in range(len(p)))
    survey_url = ref['previsit_form_url']
    
    # now craft the email
    email = "<p>Dear " + principals + ",</p><p>This is reminding you that there is a <b>November 21</b> deadline to complete the 8-week progress monitoring pre-visit form. To go directly to your school's form, please <a href=\""+survey_url+"\">click here.</a></p><p>Once this form is completed, your senior associate, " + senior_associate + ", will contact you to schedule the school visit to discuss your responses and to provide additional support.</p>"
    if status == 'AFTERSELECT':
        email += "<p>You previously selected the three goals to discuss during the meeting, but you have not filled out the form yet. After meeting with your leadership team, please continue to the form to describe the data you review to monitor progress toward these goals.</p>";
    elif status == 'RESELECT':
        email += "<p>You previously selected goals, but you didn't select 3.  Please return to the form, select 3, and then the form will be regenerated to ask specific questions about how you are tracking data.</p>";
    elif status != 'BEGIN':
        raise Exception("WHAT?!")

    email += "<p>As a reminder, The Planning & Evidence-based Support Office (PESO) has partnered with the Assistant Superintendents to support the 8 week cycle visits. The purpose is to support the Plan, Do Study, Act (PDSA) process through effective implementation, data collection, and analysis of the school comprehensives plan priority goals - but also to simplify and integrate progress monitoring so that you may find it more valuable and less time consuming.</p><p>You should meet with your leadership and/or data teams to discuss the progress you are making on your comprehensive plan priority goals and then fill out the form linked in this email, which asks 5 questions regarding your data for each goal. After filling out the pre-visit form, the PESO Senior Associate will schedule a meeting for a deeper-dive into the school's observations and analysis of data aligned to these goals and to help support your work. Your Assistant Superintendent may then review this process and can follow up with their own progress monitoring that builds off of it.</p>"

    email += "<p>To go to the goal selection form for your school, please <a href=\""+survey_url+"\">click here</a> (this is the same link as in the first line of this email).</p><p>If you have any questions, please do not hesitate to reach out to your Senior Associate.</p><p>Thank you,</p><p>Planning and Evidence-Based Support Office</p>"

    # now add to the mail queue
    mailqueue.queue_mail(
        to=emails,
        subject='8-Week Cycle Progress Monitoring Reminder',
        html_text=email,
        no_reply=True,
    ) 

            
    
def determine_progress(slp):

    # get the drive folder
    pm = GoogleDrive.Sheets.SpreadSheet(slp.sheet_service, PROGRESS_MONTORING_SHEET_ID, load_grid=True)

    mailqueue = KMail()
    
#    mailqueue = GoogleDrive.Sheets.SpreadSheet(slp.sheet_service, MAILER).get_sheet('Mail Queue')
    
    test_html = '<html><body>'
    
    for network in pm.sheets:

        if network == 'Sheet1':
            continue
        
        stats = {
            'no_progress':[],
            'selected_goals':[],
            'previsit_complete':[],
            'cycle_complete':[],
        }
        
        sheet = pm.sheets[network]
        matrix = sheet.grid_matrixb()
        for school in matrix.hashmap_matrix():
            if not school['school_name'] and not school['form_id']:
                continue
            if school['peso_visit_completed'] == 'Yes':
                stats['cycle_complete'].append(school)
            elif school['principal_completed_responses'] == 'Yes':
                stats['previsit_complete'].append(school)
            elif school['principal_selected_goals'] == 'Yes':
                stats['selected_goals'].append(school)
            else:
                stats['no_progress'].append(school)
            
        email = "Hello,<br><br>The following is a status update for <b>" + network + "</b> as of <b>" + datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p") + "</b><br><br>"

        if len(stats['cycle_complete']):
            email += '<B>' + str(len(stats['cycle_complete'])) + ' Schools Have Completed the Process:</B><ul>'
            for school in stats['cycle_complete']:
                email += fmt_bullet(school['school_name'])
            email += '</ul><br />'

        if len(stats['previsit_complete']):
            email += '<B>' + str(len(stats['previsit_complete'])) + ' Schools Have Completed the Pre-Visit Form.</B> The link will take you to the <i>Senior Associate PM Visit form</i><ul>'
            for school in stats['previsit_complete']:
                email += fmt_bullet(school['school_name'], school['cycle_visit_url'])
            email += '</ul><br />'

        if len(stats['selected_goals']):
            email += '<B>' + str(len(stats['selected_goals'])) + ' Schools Have Selected Goals but not completed the Pre-Visit form</B> (Pre-Visit Form Link Provided):<ul>'
            for school in stats['selected_goals']:
                email += fmt_bullet(school['school_name'], school['previsit_url'])
            email += '</ul><br />'
            
        if len(stats['no_progress']):
            email += '<B>' + str(len(stats['no_progress'])) + ' Schools have made no progress on this cycle.</B> (Pre-Visit Form Link Provided):<ul>'
            for school in stats['no_progress']:
                try:
                    email += fmt_bullet(school['school_name'], school['previsit_url'])
                except Exception as e:
                    import pdb
                    pdb.set_trace()
                    raise(e)
                
            email += '</ul><br />'


        # now add to the mail queue
        mailqueue.queue_mail(
            to=NETASSIGN[network.strip()],
            subject='8-Week Cycle Progress Monitoring',
            html_text=email,
            sender_name='Auto-Mailer',
        ) 
        test_html += '<br><br><hr><br><br>' + email
    test_html += '</body></html>'
    print(test_html)
            


def delinquent(slp):

    # get the drive folder
    pm = GoogleDrive.Sheets.SpreadSheet(slp.sheet_service, PROGRESS_MONTORING_SHEET_ID, load_grid=True)

    mailqueue = KMail()
    
    test_html = '<html><body>'

    school_mailer = {}
    with open("OHMYGOD.pckl", 'rb') as fh:
        everything = pickle.load(fh)
        for sid, ref in everything.items():
            if 'slp_school_name' not in ref:
                continue
            if ref['slp_school_name'] in school_mailer:
                raise Exception(":(")
            school_mailer[ ref['slp_school_name'] ] = ref

    allemails = {
        'no_progress_emails':[],
        'selected_goals_emails':[],
    }

    email = ""


    for network in pm.sheets:

        if network == 'Sheet1':
            continue
        
        stats = {
            'no_progress':[],
            'selected_goals':[],
            'no_progress_emails':[],
            'selected_goals_emails':[],
        }

        sheet = pm.sheets[network]
        matrix = sheet.grid_matrixb()
        for school in matrix.hashmap_matrix():
            if school['school_name'] is None:
                continue
                
            ref = school_mailer[school['school_name']]
            p = ref['email']['sy2017-2018_principal'].splitlines()
#            import pdb
#            pdb.set_trace()
            if p[0] == 'Sharon Marino':
                p = [p[0] + ' and ' + p[1]]
                e = [ref['email']['email'].strip()]
            else:
                e = ref['email']['email'].splitlines()
            principals = ' and '.join(p)
            emails = ', '.join(e)

            
            if not school['school_name'] and not school['form_id']:
                continue
            
            if school['principal_completed_responses'] == 'Yes':
                continue
            
            if school['principal_selected_goals'] == 'Yes':
                stats['selected_goals'].append(principals)
                stats['selected_goals_emails'].append(emails)
                allemails['selected_goals_emails'].append(emails)
            else :
                stats['no_progress'].append(principals)
                stats['no_progress_emails'].append(emails)
                allemails['no_progress_emails'].append(emails)
            
        if len(stats['selected_goals']) or len(stats['no_progress']):

            email += "<br><br><h3>" + network + "</h3>"
            if len(stats['selected_goals']):
                email += "<br><br><b>These Principals Selected Goals but did not fill them out:</b><br><br>" + ", ".join(stats['selected_goals']) + "<br><br>" + ", ".join(stats['selected_goals_emails'])
            
            if len(stats['no_progress']):
                email += "<br><br><b>These Principals have not filled out the pre-visit form and either did not select goals or are MS/HS and don't have to:</b><br><br>"+ ", ".join(stats['no_progress']) + "<br><br>"  + ", ".join(stats['no_progress_emails'])

                
    introduction = "Hello,<br><br>The following are all of the schools that have not made appropriate progress on the pre-visit form"
                
    if len(stats['selected_goals']):
        introduction += "<br><br><b>All Principals, All Networks - Selected Goals</b><br><br>" +  ", ".join(allemails['selected_goals_emails'])
            
    if len(stats['no_progress']):
        introduction += "<br><br><b>All Principals, All Networks - No Progress</b><br><br>" +  ", ".join(allemails['no_progress_emails'])

    # now add to the mail queue
    mailqueue.queue_mail(
        to='kcrouse@philasd.org',
        subject='All of the principals',
        html_text=introduction + '<br><br>' + email,
        sender_name='Auto-Mailer',
        ) 
            
    
main()    
