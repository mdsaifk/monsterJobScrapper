from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import os
from monsterJobScrapper.monsterJobScrapperDAO import monsterJobScrapper



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def homepage():
    return render_template('index.html')


@app.route('/searchJob', methods=['GET', 'POST'])
@cross_origin()
def search():
    if request.method == 'POST':
        searchString = request.form['jobtitle'].split()
        searchString = searchString[0] + '-' + searchString[1]
        jobTitle = searchString
        location = request.form['location'].replace(" ", "")
        try:
            monster = monsterJobScrapper()
            monster_url = monster.createUrl(jobTitle, location)
            bigboxes = monster.get_webPage(monster_url)
            jobs=[]

            for box in bigboxes:
                try:
                    job_link = box.find("div", {"class": "job-tittle"}).h3.a['href']
                except:
                    job_link =  "Not Found"
                try:
                    job_title = box.find("div", {"class": "job-tittle"}).h3.a.text
                except:
                    job_title =  "Not Found"
                try:
                    company_name = box.find("div", {"class": "job-tittle"}).span.a.text
                except:
                    company_name = "Not Found"
                try:
                    job_location = box.find("div", {"class": "job-tittle"}).div.span.small.text.strip()
                except:
                    job_location = "Not Found"
                try:
                    skill_box = box.find("p", {"class": "descrip-skills"}).findAll("label",{"class":"grey-link"})
                    skills=[]
                    for skill in skill_box:
                        all_skill = skill.a.text.strip(",")
                        skills.append(all_skill.replace("\n",""))
                    allSkills = ""
                    for sk in skills:
                        allSkills += sk

                except:
                    skills = "Not Found"

                mydict = {"Job Link": job_link, "Job Title": job_title, "Company Name": company_name, "Job Location": job_location,
                          "Skills": allSkills}  # saving that details to a dictionary

                jobs.append(mydict)
            return render_template('results.html', jobs=jobs)
        except Exception as e:
            print(e)
    else:
        return render_template('index.html')



port = int(os.getenv("PORT"))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=port)