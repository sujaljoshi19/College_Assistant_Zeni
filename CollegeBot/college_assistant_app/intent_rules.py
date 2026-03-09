import re

INTENT_RULES = [
    # =========================
    # ZENI IDENTITY
    # =========================
    {
        "intent": "zeni_identity",
        "patterns": [
            r"\bhow are you\b",
            r"\bwho are you\b",
            r"\bwhat is your name\b",
            r"\bwhat's your name\b",
            r"\bare you a college assistant\b",
            r"\btell me about yourself\b",
            r"\bintroduce yourself\b"
        ],
        "response": (
            "I am ZENI, your college assistant and guide for "
            "Graphic Era Hill University, Bhimtal Campus."
        )
    },

    {
        "intent": "zeni_founders",
        "patterns": [
            r"\bfounder.*zeni\b",
            r"\bfounded.*zeni\b",
            r"\bzeni.*founder\b",
            r"\bwho.*founder.*zeni\b",
            r"\bwho.*founded.*zeni\b",
            r"\bwho.*created.*zeni\b",
            r"\bwho.*made.*zeni\b",
            r"\bwho.*built.*zeni\b",
            r"\bwho.*developed.*zeni\b",
            r"\bco.?founder.*zeni\b",
            r"\bco.?founded.*zeni\b",
            r"\bzeni.*co.?founder\b",
            r"\bfounder.*you\b",
            r"\bfounded.*you\b",
            r"\bwho.*founder.*you\b",
            r"\bwho.*founded.*you\b",
            r"\bwho.*created.*you\b",
            r"\bwho.*made.*you\b",
            r"\bwho.*built.*you\b",
            r"\bwho.*developed.*you\b",
            r"\bco.?founder.*you\b",
            r"\bco.?founded.*you\b",
            r"\byour.*founder\b",
            r"\byour.*creator\b",
            r"\byour.*co.?founder\b"
        ],
        "response": (
            "I was created by Shankar Singh Bisht and Sujal Joshi, B.Tech CSE AIML students (Batch 2023 to 2027)."
        )
    },

    # =========================
    # COLLEGE IDENTITY
    # =========================
    {
        "intent": "college_name",
        "patterns": [
            # Direct name questions
            r"\bname.*college\b",
            r"\bname.*of.*college\b",
            r"\bname.*this.*college\b",
            r"\bname.*the.*college\b",
            r"\bwhat.*name.*college\b",
            r"\bwhat.*is.*name.*college\b",
            r"\bwhat.*college.*name\b",
            r"\bcollege.*name\b",
            r"\bwhich.*college\b",
            r"\bwhich.*college.*this\b",
            r"\bwhat.*college\b",
            r"\bwhat.*is.*college\b",
            r"\bwhat.*this.*college\b",
            # University name questions
            r"\bname.*university\b",
            r"\bname.*of.*university\b",
            r"\bname.*this.*university\b",
            r"\bname.*the.*university\b",
            r"\bwhat.*name.*university\b",
            r"\bwhat.*is.*name.*university\b",
            r"\bwhat.*university.*name\b",
            r"\buniversity.*name\b",
            r"\bwhich.*university\b",
            r"\bwhich.*university.*this\b",
            r"\bwhat.*university\b",
            r"\bwhat.*is.*university\b",
            r"\bwhat.*this.*university\b",
            # Institution name
            r"\bname.*institution\b",
            r"\bwhat.*institution\b",
            r"\bwhich.*institution\b"
        ],
        "response": (
            "The name of the college is Graphic Era Hill University, Bhimtal Campus."
        )
    },

    {
        "intent": "campus_overview",
        "patterns": [
            # Direct campus questions
            r"\btell.*about.*campus\b",
            r"\btell.*me.*about.*campus\b",
            r"\babout.*campus\b",
            r"\babout.*the.*campus\b",
            r"\babout.*this.*campus\b",
            r"\bwhat.*campus\b",
            r"\bwhat.*is.*campus\b",
            r"\bwhat.*this.*campus\b",
            r"\bwhat.*the.*campus\b",
            r"\bdescribe.*campus\b",
            r"\bcampus.*info\b",
            r"\bcampus.*information\b",
            r"\bcampus.*details\b",
            r"\bcampus.*overview\b",
            r"\binfo.*campus\b",
            r"\binformation.*campus\b",
            r"\bdetails.*campus\b",
            # Bhimtal specific
            r"\babout.*bhimtal\b",
            r"\babout.*bhimtal.*campus\b",
            r"\btell.*about.*bhimtal\b",
            r"\btell.*me.*about.*bhimtal\b",
            r"\bwhat.*bhimtal\b",
            r"\bwhat.*is.*bhimtal\b",
            r"\bwhat.*bhimtal.*campus\b",
            r"\bdescribe.*bhimtal\b",
            r"\bbhimtal.*info\b",
            r"\bbhimtal.*information\b",
            r"\bbhimtal.*details\b",
            r"\bbhimtal.*overview\b",
            r"\binfo.*bhimtal\b",
            r"\binformation.*bhimtal\b",
            r"\bdetails.*bhimtal\b",
            # GEHU Bhimtal
            r"\btell.*about.*gehu.*bhimtal\b",
            r"\btell.*me.*about.*gehu.*bhimtal\b",
            r"\babout.*gehu.*bhimtal\b",
            r"\bwhat.*gehu.*bhimtal\b",
            r"\bwhat.*is.*gehu.*bhimtal\b",
            r"\bdescribe.*gehu.*bhimtal\b",
            r"\bgehu.*bhimtal.*info\b",
            r"\bgehu.*bhimtal.*information\b",
            r"\bgehu.*bhimtal.*details\b",
            r"\bgehu.*bhimtal.*overview\b",
            # GEHU general
            r"\btell.*about.*gehu\b",
            r"\btell.*me.*about.*gehu\b",
            r"\babout.*gehu\b",
            r"\bwhat.*gehu\b",
            r"\bwhat.*is.*gehu\b",
            r"\bdescribe.*gehu\b",
            r"\bgehu.*info\b",
            r"\bgehu.*information\b",
            r"\bgehu.*details\b",
            r"\bgehu.*overview\b",
            # Graphic Era
            r"\btell.*about.*graphic.*era\b",
            r"\btell.*me.*about.*graphic.*era\b",
            r"\babout.*graphic.*era\b",
            r"\bwhat.*graphic.*era\b",
            r"\bwhat.*is.*graphic.*era\b",
            r"\bdescribe.*graphic.*era\b",
            r"\bgraphic.*era.*info\b",
            r"\bgraphic.*era.*information\b",
            r"\bgraphic.*era.*details\b",
            r"\bgraphic.*era.*overview\b",
            # How/what questions about campus
            r"\bhow.*campus\b",
            r"\bwhat.*campus.*like\b",
            r"\bwhats.*campus\b",
            r"\bwhat's.*campus\b",
            # University/College general
            r"\btell.*about.*university\b",
            r"\btell.*me.*about.*university\b",
            r"\babout.*university\b",
            r"\babout.*this.*university\b",
            r"\bwhat.*university\b",
            r"\bwhat.*is.*university\b",
            r"\bwhat.*this.*university\b",
            r"\bdescribe.*university\b",
            r"\buniversity.*info\b",
            r"\buniversity.*information\b",
            r"\buniversity.*details\b",
            r"\buniversity.*overview\b",
            r"\btell.*about.*college\b",
            r"\btell.*me.*about.*college\b",
            r"\babout.*college\b",
            r"\babout.*this.*college\b",
            r"\bwhat.*college\b",
            r"\bwhat.*is.*college\b",
            r"\bwhat.*this.*college\b",
            r"\bdescribe.*college\b",
            r"\bcollege.*info\b",
            r"\bcollege.*information\b",
            r"\bcollege.*details\b",
            r"\bcollege.*overview\b",
            # Location/Establishment
            r"\bwhen.*established\b",
            r"\bwhen.*was.*established\b",
            r"\bwhen.*founded\b",
            r"\bwhen.*was.*founded\b",
            r"\bwhere.*campus\b",
            r"\bwhere.*is.*campus\b",
            r"\bwhere.*bhimtal\b",
            r"\bwhere.*is.*bhimtal\b",
            r"\blocation.*campus\b",
            r"\blocation.*bhimtal\b",
            # Recognition/Accreditation
            r"\bnaac\b",
            r"\bnaac.*grade\b",
            r"\bnaac.*rating\b",
            r"\bucg.*recognized\b",
            r"\bucg.*recognition\b",
            r"\brecognized.*ucg\b",
            r"\baccredited\b",
            r"\baccreditation\b"
        ],
        "response": (
            "Established in 2011, Graphic Era Hill University (GEHU), Bhimtal "
            "is a private university located in the Kumaon foothills of the Himalayas. "
            "It is recognized by the UGC and holds an A+ grade from NAAC."
        )
    },

    # =========================
    # MANAGEMENT & AUTHORITIES
    # =========================
    {
        "intent": "campus_director",
        "patterns": [
            # Director questions
            r"\bdirector.*bhimtal\b",
            r"\bdirector.*campus\b",
            r"\bdirector.*this.*campus\b",
            r"\bdirector.*the.*campus\b",
            r"\bdirector.*gehu.*bhimtal\b",
            r"\bdirector.*of.*bhimtal\b",
            r"\bdirector.*of.*campus\b",
            r"\bdirector.*of.*bhimtal.*campus\b",
            # Who is director
            r"\bwho.*director\b",
            r"\bwho.*is.*director\b",
            r"\bwho.*director.*campus\b",
            r"\bwho.*director.*bhimtal\b",
            r"\bwho.*director.*this.*campus\b",
            r"\bwho.*director.*of.*campus\b",
            r"\bwho.*director.*of.*bhimtal\b",
            r"\bwho.*director.*of.*bhimtal.*campus\b",
            r"\bwho.*is.*director.*campus\b",
            r"\bwho.*is.*director.*bhimtal\b",
            r"\bwho.*is.*director.*of.*campus\b",
            r"\bwho.*is.*director.*of.*bhimtal\b",
            # Name of director
            r"\bname.*director\b",
            r"\bname.*of.*director\b",
            r"\bname.*director.*campus\b",
            r"\bname.*director.*bhimtal\b",
            r"\bwhat.*name.*director\b",
            r"\bwhat.*is.*name.*director\b",
            # Tell me about director
            r"\btell.*about.*director\b",
            r"\btell.*me.*about.*director\b",
            r"\binfo.*director\b",
            r"\binformation.*director\b",
            r"\bdetails.*director\b"
        ],
        "response": (
            "The Director of Graphic Era Hill University, Bhimtal Campus "
            "is Colonel A. K. Nair."
        )
    },

    {
        "intent": "university_founder",
        "patterns": [
            # Founder questions
            r"\bfounder.*graphic.*era\b",
            r"\bfounder.*of.*graphic.*era\b",
            r"\bfounded.*graphic.*era\b",
            r"\bwho.*founder.*graphic.*era\b",
            r"\bwho.*founded.*graphic.*era\b",
            r"\bwho.*is.*founder.*graphic.*era\b",
            r"\bwho.*is.*founder.*of.*graphic.*era\b",
            r"\bname.*founder.*graphic.*era\b",
            r"\bname.*of.*founder.*graphic.*era\b",
            # Chairman questions
            r"\bchairman.*graphic.*era\b",
            r"\bchairman.*of.*graphic.*era\b",
            r"\bwho.*chairman.*graphic.*era\b",
            r"\bwho.*is.*chairman.*graphic.*era\b",
            r"\bwho.*is.*chairman.*of.*graphic.*era\b",
            r"\bname.*chairman.*graphic.*era\b",
            r"\bname.*of.*chairman.*graphic.*era\b",
            # Chancellor questions
            r"\bchancellor.*graphic.*era\b",
            r"\bchancellor.*of.*graphic.*era\b",
            r"\bwho.*chancellor.*graphic.*era\b",
            r"\bwho.*is.*chancellor.*graphic.*era\b",
            r"\bwho.*is.*chancellor.*of.*graphic.*era\b",
            r"\bname.*chancellor.*graphic.*era\b",
            r"\bname.*of.*chancellor.*graphic.*era\b",
            # Owner questions
            r"\bowner.*graphic.*era\b",
            r"\bowner.*of.*graphic.*era\b",
            r"\bwho.*owner.*graphic.*era\b",
            r"\bwho.*is.*owner.*graphic.*era\b",
            r"\bwho.*is.*owner.*of.*graphic.*era\b",
            # General founder/chairman/chancellor
            r"\bfounder.*university\b",
            r"\bchairman.*university\b",
            r"\bchancellor.*university\b",
            r"\bwho.*founder.*university\b",
            r"\bwho.*chairman.*university\b",
            r"\bwho.*chancellor.*university\b",
            r"\bwho.*is.*founder.*university\b",
            r"\bwho.*is.*chairman.*university\b",
            r"\bwho.*is.*chancellor.*university\b",
            # Dr. Kamal Ghanshala specific
            r"\bkamal.*ghanshala\b",
            r"\bdr.*kamal.*ghanshala\b",
            r"\bwho.*kamal.*ghanshala\b"
        ],
        "response": (
            "Dr. Kamal Ghanshala is the Founder of Graphic Era University."
        )
    },

    # =========================
    # ACADEMICS
    # =========================
    {
        "intent": "hod_btech_cse",
        "patterns": [
            # HOD B.Tech CSE
            r"\bhod.*btech.*cse\b",
            r"\bhod.*of.*btech.*cse\b",
            r"\bhod.*btech.*computer.*science\b",
            r"\bhod.*of.*btech.*computer.*science\b",
            r"\bhead.*department.*btech.*cse\b",
            r"\bhead.*department.*btech.*computer.*science\b",
            r"\bhead.*of.*department.*btech.*cse\b",
            r"\bhead.*of.*department.*btech.*computer.*science\b",
            # HOD CSE
            r"\bhod.*cse\b",
            r"\bhod.*of.*cse\b",
            r"\bhod.*computer.*science\b",
            r"\bhod.*of.*computer.*science\b",
            r"\bhead.*department.*cse\b",
            r"\bhead.*department.*computer.*science\b",
            r"\bhead.*of.*department.*cse\b",
            r"\bhead.*of.*department.*computer.*science\b",
            # Who is HOD
            r"\bwho.*hod.*btech.*cse\b",
            r"\bwho.*hod.*cse\b",
            r"\bwho.*hod.*computer.*science\b",
            r"\bwho.*is.*hod.*btech.*cse\b",
            r"\bwho.*is.*hod.*cse\b",
            r"\bwho.*is.*hod.*computer.*science\b",
            r"\bwho.*is.*hod.*of.*btech.*cse\b",
            r"\bwho.*is.*hod.*of.*cse\b",
            r"\bwho.*is.*hod.*of.*computer.*science\b",
            # Name of HOD
            r"\bname.*hod.*btech.*cse\b",
            r"\bname.*hod.*cse\b",
            r"\bname.*hod.*computer.*science\b",
            r"\bname.*of.*hod.*btech.*cse\b",
            r"\bname.*of.*hod.*cse\b",
            r"\bname.*of.*hod.*computer.*science\b",
            # Dr. Ankur Singh Bist specific
            r"\bankur.*singh.*bist\b",
            r"\bdr.*ankur.*singh.*bist\b",
            r"\bwho.*ankur.*singh.*bist\b"
        ],
        "response": (
            "The HOD of B.Tech Computer Science Engineering is "
            "Dr. Ankur Singh Bist."
        )
    },

    {
        "intent": "hod_bca",
        "patterns": [
            # HOD BCA
            r"\bhod.*bca\b",
            r"\bhod.*of.*bca\b",
            r"\bbca.*hod\b",
            r"\bhead.*department.*bca\b",
            r"\bhead.*of.*department.*bca\b",
            r"\bhead.*bca\b",
            r"\bhead.*of.*bca\b",
            # Who is HOD BCA
            r"\bwho.*hod.*bca\b",
            r"\bwho.*is.*hod.*bca\b",
            r"\bwho.*is.*hod.*of.*bca\b",
            r"\bwho.*head.*bca\b",
            r"\bwho.*is.*head.*bca\b",
            r"\bwho.*is.*head.*of.*bca\b",
            # Name of HOD BCA
            r"\bname.*hod.*bca\b",
            r"\bname.*of.*hod.*bca\b",
            r"\bname.*head.*bca\b",
            r"\bname.*of.*head.*bca\b",
            # Dr. Sandeep Kumar Budhani specific
            r"\bsandeep.*kumar.*budhani\b",
            r"\bdr.*sandeep.*kumar.*budhani\b",
            r"\bwho.*sandeep.*kumar.*budhani\b"
        ],
        "response": (
            "The HOD of BCA is Dr. Sandeep Kumar Budhani."
        )
    },

    {
        "intent": "courses_availability",
        "patterns": [
            # B.Tech availability
            r"\bbtech.*available\b",
            r"\bis.*btech.*available\b",
            r"\bdoes.*btech.*available\b",
            r"\bbtech.*offered\b",
            r"\bis.*btech.*offered\b",
            r"\bdoes.*btech.*offered\b",
            r"\bbtech.*course\b",
            r"\bbtech.*program\b",
            # BCA availability
            r"\bbca.*available\b",
            r"\bis.*bca.*available\b",
            r"\bdoes.*bca.*available\b",
            r"\bbca.*offered\b",
            r"\bis.*bca.*offered\b",
            r"\bdoes.*bca.*offered\b",
            r"\bbca.*course\b",
            r"\bbca.*program\b",
            # Courses general
            r"\bcourses.*bhimtal\b",
            r"\bcourses.*offered\b",
            r"\bcourses.*available\b",
            r"\bwhat.*courses\b",
            r"\bwhat.*courses.*bhimtal\b",
            r"\bwhat.*courses.*offered\b",
            r"\bwhat.*courses.*available\b",
            r"\bwhich.*courses\b",
            r"\bwhich.*courses.*bhimtal\b",
            r"\bwhich.*courses.*offered\b",
            r"\bwhich.*courses.*available\b",
            r"\btell.*about.*courses\b",
            r"\btell.*me.*about.*courses\b",
            r"\binfo.*courses\b",
            r"\binformation.*courses\b",
            r"\bdetails.*courses\b",
            r"\blist.*courses\b",
            r"\bcourse.*list\b",
            # Programs general
            r"\bprograms.*bhimtal\b",
            r"\bprograms.*offered\b",
            r"\bprograms.*available\b",
            r"\bwhat.*programs\b",
            r"\bwhat.*programs.*bhimtal\b",
            r"\bwhat.*programs.*offered\b",
            r"\bwhat.*programs.*available\b",
            r"\bwhich.*programs\b",
            r"\bwhich.*programs.*bhimtal\b",
            r"\bwhich.*programs.*offered\b",
            r"\bwhich.*programs.*available\b",
            r"\btell.*about.*programs\b",
            r"\btell.*me.*about.*programs\b",
            r"\binfo.*programs\b",
            r"\binformation.*programs\b",
            r"\bdetails.*programs\b",
            r"\blist.*programs\b",
            r"\bprogram.*list\b",
            # Degree questions
            r"\bdegrees.*offered\b",
            r"\bdegrees.*available\b",
            r"\bwhat.*degrees\b",
            r"\bwhich.*degrees\b",
            # Specific course questions
            r"\bmba.*available\b",
            r"\bmca.*available\b",
            r"\bmtech.*available\b",
            r"\bdiploma.*available\b",
            r"\bnursing.*available\b",
            r"\bpharmacy.*available\b"
        ],
        "response": (
            "Yes, a wide range of programs are offered, including B.Tech, BCA, diploma programs, management courses, postgraduate programs, nursing, and pharmacy courses. "
            "Graphic Era Hill University, Bhimtal Campus."
        )
    },

    # =========================
    # FACILITIES & CAMPUS LIFE
    # =========================
    {
        "intent": "hostel_facility",
        "patterns": [
            # Hostel availability
            r"\bhostel.*available\b",
            r"\bis.*hostel.*available\b",
            r"\bdoes.*hostel.*available\b",
            r"\bhostel.*facility\b",
            r"\bhostel.*facilities\b",
            r"\bis.*hostel.*facility\b",
            r"\bdoes.*hostel.*facility\b",
            # Campus hostel
            r"\bcampus.*hostel\b",
            r"\bhostel.*campus\b",
            r"\bdoes.*campus.*hostel\b",
            r"\bdoes.*campus.*have.*hostel\b",
            r"\bis.*there.*hostel\b",
            r"\bis.*there.*hostel.*campus\b",
            # Hostel questions
            r"\bhostel\b",
            r"\babout.*hostel\b",
            r"\btell.*about.*hostel\b",
            r"\btell.*me.*about.*hostel\b",
            r"\binfo.*hostel\b",
            r"\binformation.*hostel\b",
            r"\bdetails.*hostel\b",
            r"\bhostel.*info\b",
            r"\bhostel.*information\b",
            r"\bhostel.*details\b",
            # Accommodation
            r"\baccommodation\b",
            r"\baccommodation.*available\b",
            r"\bis.*accommodation.*available\b",
            r"\bdoes.*accommodation\b",
            r"\bstudent.*accommodation\b",
            r"\bhostel.*accommodation\b",
            # Boarding
            r"\bboarding\b",
            r"\bboarding.*facility\b",
            r"\bboarding.*available\b"
        ],
        "response": (
            "Yes, hostel facilities are available at "
            "Graphic Era Hill University, Bhimtal Campus."
        )
    },

    {
        "intent": "library_facility",
        "patterns": [
            # Library availability
            r"\blibrary.*available\b",
            r"\bis.*library.*available\b",
            r"\bdoes.*library.*available\b",
            r"\blibrary.*facility\b",
            r"\blibrary.*facilities\b",
            r"\bis.*library.*facility\b",
            r"\bdoes.*library.*facility\b",
            # Is there library
            r"\bis.*library\b",
            r"\bis.*there.*library\b",
            r"\bdoes.*library\b",
            r"\bdoes.*campus.*library\b",
            r"\bdoes.*campus.*have.*library\b",
            # Campus library
            r"\bcampus.*library\b",
            r"\blibrary.*campus\b",
            r"\bthere.*library\b",
            # Library questions
            r"\babout.*library\b",
            r"\btell.*about.*library\b",
            r"\btell.*me.*about.*library\b",
            r"\binfo.*library\b",
            r"\binformation.*library\b",
            r"\bdetails.*library\b",
            r"\blibrary.*info\b",
            r"\blibrary.*information\b",
            r"\blibrary.*details\b",
            # Library timings/hours
            r"\blibrary.*timing\b",
            r"\blibrary.*timings\b",
            r"\blibrary.*hours\b",
            r"\blibrary.*time\b",
            r"\bwhen.*library.*open\b",
            r"\bwhen.*library.*close\b"
        ],
        "response": (
            "Yes, the campus has a well-equipped library for students."
        )
    },

    {
        "intent": "wifi_facility",
        "patterns": [
            # WiFi availability
            r"\bwifi.*available\b",
            r"\bis.*wifi.*available\b",
            r"\bdoes.*wifi.*available\b",
            r"\bwifi.*facility\b",
            r"\bwifi.*facilities\b",
            r"\bis.*wifi.*facility\b",
            r"\bdoes.*wifi.*facility\b",
            # WiFi campus
            r"\bwifi.*campus\b",
            r"\bcampus.*wifi\b",
            r"\bis.*wifi\b",
            r"\bis.*wifi.*campus\b",
            r"\bdoes.*campus.*wifi\b",
            r"\bdoes.*campus.*have.*wifi\b",
            r"\bis.*there.*wifi\b",
            r"\bis.*there.*wifi.*campus\b",
            # WiFi questions
            r"\babout.*wifi\b",
            r"\btell.*about.*wifi\b",
            r"\btell.*me.*about.*wifi\b",
            r"\binfo.*wifi\b",
            r"\binformation.*wifi\b",
            r"\bdetails.*wifi\b",
            r"\bwifi.*info\b",
            r"\bwifi.*information\b",
            r"\bwifi.*details\b",
            # Wireless internet
            r"\bwireless.*internet\b",
            r"\bwireless.*available\b",
            r"\bis.*wireless.*internet\b",
            r"\bdoes.*wireless.*internet\b",
            # Internet connectivity
            r"\binternet.*campus\b",
            r"\binternet.*available\b",
            r"\bis.*internet.*available\b",
            r"\bdoes.*internet.*available\b",
            r"\binternet.*connectivity\b",
            r"\bis.*internet.*connectivity\b",
            r"\bnetwork.*campus\b",
            r"\bnetwork.*available\b",
            # WiFi speed/connection
            r"\bwifi.*speed\b",
            r"\bwifi.*connection\b",
            r"\bwifi.*connectivity\b"
        ],
        "response": (
            "Yes, WiFi connectivity is available across the campus."
        )
    },

    # =========================
    # PLACEMENTS
    # =========================
    {
        "intent": "placements",
        "patterns": [
            # Placement cell
            r"\bplacement.*cell\b",
            r"\bplacement.*cell.*available\b",
            r"\bis.*placement.*cell\b",
            r"\bdoes.*placement.*cell\b",
            r"\bplacement.*cell.*bhimtal\b",
            # Placements available
            r"\bplacements.*available\b",
            r"\bis.*placements.*available\b",
            r"\bdoes.*placements.*available\b",
            r"\bplacement.*available\b",
            r"\bis.*placement.*available\b",
            r"\bdoes.*placement.*available\b",
            # Placement questions
            r"\bplacement\b",
            r"\bplacements\b",
            r"\babout.*placement\b",
            r"\babout.*placements\b",
            r"\btell.*about.*placement\b",
            r"\btell.*about.*placements\b",
            r"\btell.*me.*about.*placement\b",
            r"\btell.*me.*about.*placements\b",
            r"\binfo.*placement\b",
            r"\binfo.*placements\b",
            r"\binformation.*placement\b",
            r"\binformation.*placements\b",
            r"\bdetails.*placement\b",
            r"\bdetails.*placements\b",
            # Placement Bhimtal/GEHU
            r"\bplacement.*bhimtal\b",
            r"\bplacements.*bhimtal\b",
            r"\bplacement.*gehu\b",
            r"\bplacements.*gehu\b",
            r"\bdoes.*gehu.*placements\b",
            r"\bdoes.*gehu.*placement\b",
            r"\bdoes.*bhimtal.*placements\b",
            r"\bdoes.*bhimtal.*placement\b",
            # Placement opportunities
            r"\bplacement.*opportunities\b",
            r"\bplacement.*opportunity\b",
            r"\bjob.*placement\b",
            r"\bjob.*placements\b",
            r"\bplacement.*job\b",
            r"\bplacements.*job\b",
            # Career/Jobs
            r"\bcareer.*placement\b",
            r"\bcareer.*placements\b",
            r"\bjob.*opportunities\b",
            r"\bjob.*opportunity\b",
            r"\bcareer.*opportunities\b",
            r"\bcareer.*opportunity\b",
            # Placement statistics/records
            r"\bplacement.*statistics\b",
            r"\bplacement.*stats\b",
            r"\bplacement.*record\b",
            r"\bplacement.*records\b",
            r"\bplacement.*data\b",
            r"\bplacement.*percentage\b",
            r"\bplacement.*rate\b",
            # Companies/Recruiters
            r"\bplacement.*companies\b",
            r"\bplacement.*company\b",
            r"\bcompanies.*visit\b",
            r"\bcompanies.*campus\b",
            r"\brecruiters\b",
            r"\bplacement.*recruiters\b"
        ],
        "response": (
            "Yes, Graphic Era Hill University, Bhimtal Campus "
            "has a dedicated placement cell to support students."
        )
    }
]


def match_intent(user_query: str):
    """
    Match user query against predefined intent rules.
    
    Args:
        user_query: The user's query string (should be in English)
    
    Returns:
        str: Fixed response if intent matches, None otherwise
    """
    if not user_query:
        return None

    query = user_query.lower().strip()

    for rule in INTENT_RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, query):
                return rule["response"]

    return None