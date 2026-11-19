import json
import os

expanded_regulations = [
    # --- MODULES & SEMESTRES (1-10) ---
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Modalités d'inscription et obligation d'assiduité",
        "resume": "L'inscription administrative est obligatoire pour tous les étudiants en début d'année universitaire à l'UIT. L'assiduité à tous les cours magistraux, TD et TP est rigoureusement obligatoire.",
        "lien": "https://uit.edu.tn/reglement/inscription-assiduite",
        "date": "Mon, 01 Sep 2026 08:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Administrative Registration and Attendance Policy",
        "resume": "Administrative registration is mandatory for all students at UIT at the beginning of each academic year. Attendance at all lectures, tutorials, and practical labs is strictly required.",
        "lien": "https://uit.edu.tn/reglement/registration-attendance",
        "date": "Mon, 01 Sep 2026 08:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Régime des absences et des justificatifs médicaux",
        "resume": "Toute absence à une séance de TD ou de TP doit être justifiée par un certificat médical dans un délai de 48 heures. Au-delà de 3 absences injustifiées par module, l'étudiant reçoit un avertissement officiel.",
        "lien": "https://uit.edu.tn/reglement/regime-absences",
        "date": "Mon, 01 Sep 2026 09:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Absence Policy and Medical Certificates",
        "resume": "Any absence from tutorials or practical sessions must be justified by a medical certificate within 48 hours. Beyond 3 unjustified absences per module, the student receives an official warning.",
        "lien": "https://uit.edu.tn/reglement/absence-policy",
        "date": "Mon, 01 Sep 2026 09:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Conditions de validation des modules et des semestres",
        "resume": "Un module est validé si la note obtenue est supérieure ou égale à 10 sur 20. Le semestre est validé si la moyenne générale des notes de toutes les unités d'enseignement est supérieure ou égale à 10/20 sans note éliminatoire.",
        "lien": "https://uit.edu.tn/reglement/validation-semestre",
        "date": "Mon, 01 Sep 2026 10:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Module and Semester Validation Criteria",
        "resume": "A module is validated if the grade obtained is greater than or equal to 10 out of 20. The semester is validated if the overall weighted average is at least 10/20 with no elimination grade.",
        "lien": "https://uit.edu.tn/reglement/semester-validation",
        "date": "Mon, 01 Sep 2026 10:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Organisation de la session de rattrapage",
        "resume": "Les étudiants n'ayant pas validé leur semestre lors de la session principale peuvent se présenter à la session de rattrapage. La note de rattrapage remplace définitivement la note précédente.",
        "lien": "https://uit.edu.tn/reglement/session-rattrapage",
        "date": "Mon, 01 Sep 2026 11:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Make-up Exam Session Organization",
        "resume": "Students who fail to validate their semester during the main session may sit for the make-up session. The make-up exam grade permanently replaces the previous grade.",
        "lien": "https://uit.edu.tn/reglement/makeup-session",
        "date": "Mon, 01 Sep 2026 11:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Sanctions en cas de fraude aux examens",
        "resume": "Tout cas de fraude ou de tentative de fraude lors d'un examen entraîne la saisine immédiate du conseil de discipline de l'UIT et l'attribution de la note zéro à l'épreuve concernée.",
        "lien": "https://uit.edu.tn/reglement/fraude-examens",
        "date": "Mon, 01 Sep 2026 12:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Sanctions for Exam Fraud",
        "resume": "Any case or attempted case of exam fraud leads to an immediate referral to the UIT disciplinary board and the assignment of a zero grade for the corresponding test.",
        "lien": "https://uit.edu.tn/reglement/exam-fraud",
        "date": "Mon, 01 Sep 2026 12:00:00 +0000"
    },

    # --- APPRENTISSAGE & ALTERNANCE (11-20) ---
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Règles du cycle ingénieur en alternance",
        "resume": "Le cycle ingénieur en alternance à l'UIT combine des périodes d'enseignement académique à l'université et des périodes de stage pratique en entreprise sous contrat de travail.",
        "lien": "https://uit.edu.tn/reglement/alternance-cycle",
        "date": "Mon, 01 Sep 2026 13:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Apprenticeship Engineering Cycle Rules",
        "resume": "The apprenticeship engineering cycle at UIT combines academic teaching periods at the university and practical work periods in a company under an employment contract.",
        "lien": "https://uit.edu.tn/reglement/apprenticeship-cycle",
        "date": "Mon, 01 Sep 2026 13:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Évaluation de la période en entreprise",
        "resume": "L'évaluation en entreprise pour les apprentis de l'UIT repose sur un rapport technique soutenu devant un jury mixte composé d'universitaires et de tuteurs professionnels.",
        "lien": "https://uit.edu.tn/reglement/evaluation-entreprise",
        "date": "Mon, 01 Sep 2026 14:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Company Period Evaluation",
        "resume": "Company period evaluation for UIT apprentices is based on a technical report defended before a joint jury composed of academic professors and professional mentors.",
        "lien": "https://uit.edu.tn/reglement/company-evaluation",
        "date": "Mon, 01 Sep 2026 14:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Suivi des heures de travail et des feuilles d'émargement",
        "resume": "Les apprentis de l'UIT doivent obligatoirement valider leurs feuilles d'émargement mensuelles et enregistrer leurs heures de travail validées par l'entreprise partenaire.",
        "lien": "https://uit.edu.tn/reglement/feuilles-emargement",
        "date": "Mon, 01 Sep 2026 15:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Timesheet Tracking and Attendance Logs",
        "resume": "UIT apprentices must validate their monthly timesheets and record their work hours signed off by the partner enterprise.",
        "lien": "https://uit.edu.tn/reglement/timesheet-tracking",
        "date": "Mon, 01 Sep 2026 15:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Rupture de contrat d'alternance",
        "resume": "En cas de rupture du contrat de travail par l'entreprise partenaire, l'étudiant apprenti dispose d'un délai de 90 jours pour retrouver un nouvel employeur et maintenir son statut à l'UIT.",
        "lien": "https://uit.edu.tn/reglement/rupture-contrat",
        "date": "Mon, 01 Sep 2026 16:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Apprenticeship Contract Termination",
        "resume": "In case of work contract termination by the partner company, the apprentice student has a 90-day grace period to find a new employer and maintain their student status at UIT.",
        "lien": "https://uit.edu.tn/reglement/contract-termination",
        "date": "Mon, 01 Sep 2026 16:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Tutorat pédagogique et professionnel",
        "resume": "Chaque apprenti à l'UIT se voit attribuer un tuteur académique pour superviser ses projets universitaires et un tuteur en entreprise pour l'accompagner dans ses missions opérationnelles.",
        "lien": "https://uit.edu.tn/reglement/tutorat",
        "date": "Mon, 01 Sep 2026 17:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Academic and Professional Mentorship",
        "resume": "Each apprentice at UIT is assigned an academic tutor to supervise university projects and a company mentor to guide them through operational tasks.",
        "lien": "https://uit.edu.tn/reglement/mentorship",
        "date": "Mon, 01 Sep 2026 17:00:00 +0000"
    },

    # --- EXAMENS & NOTES (21-30) ---
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Calcul de la moyenne pondérée et coefficients",
        "resume": "La moyenne d'une unité d'enseignement est calculée en faisant la somme des produits de chaque note par son coefficient, divisée par la somme totale des coefficients.",
        "lien": "https://uit.edu.tn/reglement/calcul-moyenne",
        "date": "Mon, 01 Sep 2026 18:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Weighted Average and Coefficient Calculation",
        "resume": "The average of a teaching unit is calculated by taking the sum of each grade multiplied by its coefficient, divided by the total sum of coefficients.",
        "lien": "https://uit.edu.tn/reglement/weighted-average",
        "date": "Mon, 01 Sep 2026 18:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Modalités de consultation des copies d'examen",
        "resume": "Les étudiants disposent d'un délai de 5 jours ouvrables après l'affichage des résultats pour formuler une demande écrite de consultation de copie auprès du département.",
        "lien": "https://uit.edu.tn/reglement/consultation-copies",
        "date": "Mon, 01 Sep 2026 19:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Exam Paper Review Procedures",
        "resume": "Students have a 5-working-day window after results publication to submit a formal written request to review their exam paper with the department.",
        "lien": "https://uit.edu.tn/reglement/exam-review",
        "date": "Mon, 01 Sep 2026 19:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Procédure de réclamation de notes",
        "resume": "Toute réclamation concernant une erreur de transcription de note doit être adressée au service des examens de l'UIT par email officiel dans les 48 heures suivant la consultation.",
        "lien": "https://uit.edu.tn/reglement/reclamation-notes",
        "date": "Mon, 01 Sep 2026 20:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Grade Dispute Procedure",
        "resume": "Any dispute regarding a grade transcription error must be sent to the UIT examination office via official email within 48 hours following the paper review.",
        "lien": "https://uit.edu.tn/reglement/grade-dispute",
        "date": "Mon, 01 Sep 2026 20:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Note éliminatoire aux examens",
        "resume": "Une note inférieure à 5 sur 20 à une matière majeure ou à un projet de fin de module est considérée comme éliminatoire, empêchant la compensation du semestre.",
        "lien": "https://uit.edu.tn/reglement/note-eliminatoire",
        "date": "Mon, 01 Sep 2026 21:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Elimination Grade in Examinations",
        "resume": "A grade below 5 out of 20 in a major subject or module end project is considered an elimination grade, preventing semester grade compensation.",
        "lien": "https://uit.edu.tn/reglement/elimination-grade",
        "date": "Mon, 01 Sep 2026 21:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Absence justifiée aux examens finaux",
        "resume": "En cas d'absence justifiée par un cas de force majeure ou un certificat médical officiel lors de la session principale, l'étudiant est autorisé à passer l'examen lors de la session de rattrapage sans pénalité.",
        "lien": "https://uit.edu.tn/reglement/absence-examen",
        "date": "Mon, 01 Sep 2026 22:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Excused Absence from Final Exams",
        "resume": "In case of an excused absence due to force majeure or an official medical certificate during the main session, the student is permitted to take the exam during the make-up session without penalty.",
        "lien": "https://uit.edu.tn/reglement/excused-exam-absence",
        "date": "Mon, 01 Sep 2026 22:00:00 +0000"
    },

    # --- STAGES & PROJETS DE FIN D'ÉTUDES (31-40) ---
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Conditions d'validation du PFE (Projet de Fin d'Études)",
        "resume": "Le Projet de Fin d'Études (PFE) est obligatoire pour l'obtention du diplôme d'ingénieur de l'UIT. Il doit durer au minimum 4 mois et faire l'objet d'un mémoire écrit et d'une soutenance orale.",
        "lien": "https://uit.edu.tn/reglement/pfe-conditions",
        "date": "Mon, 01 Sep 2026 23:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Final Year Project (PFE) Validation Conditions",
        "resume": "The Final Year Project (PFE) is mandatory to obtain the UIT engineering degree. It must last at least 4 months and result in a written thesis and an oral defense.",
        "lien": "https://uit.edu.tn/reglement/pfe-conditions-en",
        "date": "Mon, 01 Sep 2026 23:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Composition du jury de soutenance de PFE",
        "resume": "Le jury de soutenance de PFE à l'UIT est composé d'au moins trois membres : un président de jury universitaire, un encadrant académique et un rapporteur ou expert professionnel.",
        "lien": "https://uit.edu.tn/reglement/jury-pfe",
        "date": "Tue, 02 Sep 2026 08:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "PFE Defense Jury Composition",
        "resume": "The PFE defense jury at UIT consists of at least three members: an academic jury president, an academic supervisor, and a professional reviewer or expert.",
        "lien": "https://uit.edu.tn/reglement/pfe-jury-en",
        "date": "Tue, 02 Sep 2026 08:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Stages d'été obligatoires",
        "resume": "Les étudiants en cycle préparatoire et ingénieur de l'UIT doivent valider des stages d'été ouvriers ou techniques d'une durée minimale de 4 semaines chaque année.",
        "lien": "https://uit.edu.tn/reglement/stages-ete",
        "date": "Tue, 02 Sep 2026 09:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Mandatory Summer Internships",
        "resume": "Students in preparatory and engineering cycles at UIT must complete mandatory worker or technical summer internships lasting at least 4 weeks each year.",
        "lien": "https://uit.edu.tn/reglement/summer-internships",
        "date": "Tue, 02 Sep 2026 09:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Validation des conventions de stage",
        "resume": "Toute convention de stage doit être signée par l'étudiant, l'entreprise d'accueil et le directeur des études de l'UIT avant le commencement effectif du stage.",
        "lien": "https://uit.edu.tn/reglement/conventions-stage",
        "date": "Tue, 02 Sep 2026 10:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Internship Agreement Validation",
        "resume": "Any internship agreement must be signed by the student, the host company, and the UIT director of studies prior to the actual start of the internship.",
        "lien": "https://uit.edu.tn/reglement/internship-agreements",
        "date": "Tue, 02 Sep 2026 10:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Confidentialité des travaux de recherche et PFE",
        "resume": "Les étudiants effectuant des projets de recherche ou des PFE en partenariat avec des entreprises industrielles peuvent demander une clause de confidentialité signée par tous les membres du jury.",
        "lien": "https://uit.edu.tn/reglement/confidentialite",
        "date": "Tue, 02 Sep 2026 11:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Confidentiality of Research and PFE Works",
        "resume": "Students conducting research projects or PFEs in partnership with industrial companies may request a confidentiality agreement signed by all jury members.",
        "lien": "https://uit.edu.tn/reglement/confidentiality",
        "date": "Tue, 02 Sep 2026 11:00:00 +0000"
    },

    # --- VIE UNIVERSITAIRE & DISCIPLINE (41-55) ---
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Règlement intérieur et utilisation du matériel informatique",
        "resume": "L'utilisation des laboratoires informatiques de l'UIT implique le respect des règles de sécurité des réseaux, l'interdiction du téléchargement illégal et le respect du matériel mis à disposition.",
        "lien": "https://uit.edu.tn/reglement/materiel-informatique",
        "date": "Tue, 02 Sep 2026 12:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Internal Regulations and Computer Equipment Usage",
        "resume": "Using UIT computer labs implies compliance with network security rules, prohibition of illegal downloading, and careful handling of provided hardware.",
        "lien": "https://uit.edu.tn/reglement/it-equipment",
        "date": "Tue, 02 Sep 2026 12:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Activités associatives et clubs étudiants",
        "resume": "L'UIT encourage la vie associative à travers les clubs culturels, scientifiques et sportifs. Toute organisation d'événement au sein du campus nécessite l'autorisation préalable de l'administration.",
        "lien": "https://uit.edu.tn/reglement/activites-associatives",
        "date": "Tue, 02 Sep 2026 13:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Student Clubs and Association Activities",
        "resume": "UIT encourages student life through cultural, scientific, and sports clubs. Any event organization on campus requires prior approval from the administration.",
        "lien": "https://uit.edu.tn/reglement/student-clubs",
        "date": "Tue, 02 Sep 2026 13:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Procédure du conseil de discipline",
        "resume": "Le conseil de discipline de l'UIT se réunit sur convocation du président de l'université en cas de manquement grave au règlement intérieur, de violence ou de tricherie avérée.",
        "lien": "https://uit.edu.tn/reglement/conseil-discipline",
        "date": "Tue, 02 Sep 2026 14:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Disciplinary Board Procedure",
        "resume": "The UIT disciplinary board convenes upon summons by the university president in cases of severe breaches of internal regulations, violence, or proven cheating.",
        "lien": "https://uit.edu.tn/reglement/disciplinary-board",
        "date": "Tue, 02 Sep 2026 14:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Échanges internationaux et mobilité académique",
        "resume": "Les étudiants de l'UIT ont la possibilité d'effectuer un semestre ou une année d'échange académique dans des universités partenaires à l'étranger sous réserve de valider tous leurs prérequis.",
        "lien": "https://uit.edu.tn/reglement/mobilite-internationale",
        "date": "Tue, 02 Sep 2026 15:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "International Exchange and Academic Mobility",
        "resume": "UIT students have the opportunity to complete an academic exchange semester or year at partner universities abroad, subject to fulfilling all prerequisite requirements.",
        "lien": "https://uit.edu.tn/reglement/international-mobility",
        "date": "Tue, 02 Sep 2026 15:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Règles d'accès et d'utilisation de la bibliothèque",
        "resume": "La bibliothèque de l'UIT met à disposition des ouvrages physiques et des ressources numériques. Le prêt de livres est limité à trois ouvrages pour une durée maximale de 15 jours renouvelables.",
        "lien": "https://uit.edu.tn/reglement/bibliotheque",
        "date": "Tue, 02 Sep 2026 16:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Library Access and Usage Rules",
        "resume": "The UIT library provides physical books and digital resources. Book loans are limited to three items for a maximum renewable period of 15 days.",
        "lien": "https://uit.edu.tn/reglement/library-rules",
        "date": "Tue, 02 Sep 2026 16:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Régime spécial pour les étudiants sportifs de haut niveau",
        "resume": "Un aménagement d'emploi du temps et des sessions d'examens spécifiques peuvent être accordés aux étudiants reconnus sportifs de haut niveau par les autorités nationales.",
        "lien": "https://uit.edu.tn/reglement/sportifs-haut-niveau",
        "date": "Tue, 02 Sep 2026 17:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Special Accommodations for High-Level Athletes",
        "resume": "Schedule adjustments and specific examination sessions may be granted to students recognized as high-level athletes by national authorities.",
        "lien": "https://uit.edu.tn/reglement/high-level-athletes",
        "date": "Tue, 02 Sep 2026 17:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Modalités de réinscription et redoublement",
        "resume": "Le redoublement est autorisé une seule fois au cours du cycle préparatoire et une seule fois au cours du cycle ingénieur de l'UIT.",
        "lien": "https://uit.edu.tn/reglement/redoublement",
        "date": "Tue, 02 Sep 2026 18:00:00 +0000"
    },
    {
        "source": "UIT Study Regulations",
        "titre": "Re-registration and Repeating Rules",
        "resume": "Repeating an academic year is permitted only once during the preparatory cycle and once during the engineering cycle at UIT.",
        "lien": "https://uit.edu.tn/reglement/repeating-rules",
        "date": "Tue, 02 Sep 2026 18:00:00 +0000"
    },
    {
        "source": "Règlement des Études UIT (Fictif)",
        "titre": "Droit de recours des étudiants",
        "resume": "Tout étudiant s'estimant lésé par une décision du jury de délibération peut saisir par écrit le président de l'UIT pour demander un examen de dossier dans un délai de 5 jours.",
        "lien": "https://uit.edu.tn/reglement/droit-recours",
        "date": "Tue, 02 Sep 2026 19:00:00 +0000"
    }
]

# Write to data folder
os.makedirs("data", exist_ok=True)
filepath = os.path.join("data", "reglement_etudes.json")
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(expanded_regulations, f, ensure_ascii=False, indent=4)

print(f"[+] Successfully generated expanded dataset with {len(expanded_regulations)} articles at {filepath}!")