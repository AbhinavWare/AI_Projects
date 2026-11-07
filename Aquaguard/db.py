#Helper file for various functions and db connection.
import mysql.connector
import bcrypt

class Database:
    def __init__(self): #Database Connection.
        self.connection = mysql.connector.connect(host = "localhost", user = "root", password = "root@123", database = "aquagaurd")
        self.cursor = self.connection.cursor(dictionary=True)
    
    def login(self,username,password):
        query = """
        select * from admin where username = %s and password = %s;
        """
        self.cursor.execute(query,(username,password))
        return self.cursor.fetchone()

    def close(self): #Closing function.
        self.cursor.close()
        self.connection.close()
    
    def get_Stats(self): #Returns dashboard stats
        query = """
        select
        count(*) as Stations,
        count(distinct state) as States,
        round(avg(ph),2) as Average_pH,
        round(avg(do_level),2) as Average_DO,
        round(avg(bod),2) as Average_BOD 
        from water_quality;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def getAll(self):
        self.cursor.execute("select * from water_quality;")
        return self.cursor.fetchall()
    
    def searchStation(self,station):
        query = """select * from water_quality where station_name like %s;"""
        self.cursor.execute(query,("%" + station + "%",))
        return self.cursor.fetchall()
    
    def search_state(self, state):
        query = """
        select *
        from water_quality
        where state=%s;
        """
        self.cursor.execute(query, (state,))
        return self.cursor.fetchall()

    def top_stations(self,choice):
        #At time of calling we can get options from gui convert it to 1 or other value.
        if choice == 1:
            self.cursor.execute("select station_name,state, pollution_index from water_quality order by pollution_index asc limit 10;") 
        else: 
            self.cursor.execute("select station_name,state, pollution_index from water_quality order by pollution_index desc limit 10;") 
        return self.cursor.fetchall()   
    
    def getCluster(self,cluster):
        query = "select * from water_quality where cluster like %s;"
        self.cursor.execute(query,(cluster,))
        return self.cursor.fetchall()
    
    def getParameters(self): #Returns dashboard stats
        query = """
        select
        round(avg(ph),2) as Average_pH,
        round(avg(do_level),2) as Average_DO,
        round(avg(bod),2) as Average_BOD,
        round(avg(nitrate),2) as nitrate,
        round(avg(fluoride),2) as fluoride,
        round(avg(conductivity),2) as conductivity
        from water_quality;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()    
        
    def state_summary(self, state):
        query = """
        select state,
        count(*) as total_stations,
        round(avg(ph), 2) as avg_ph,
        round(avg(do_level), 2) as avg_do,
        round(avg(bod), 2) as avg_bod,
        round(avg(nitrate), 2) as avg_nitrate,
        round(avg(fluoride), 2) as avg_fluoride,
        round(avg(conductivity), 2) as avg_conductivity,
        round(avg(pollution_index), 2) as avg_pollution
        from water_quality
        where state = %s
        group by state;
        """
        self.cursor.execute(query, (state,))
        return self.cursor.fetchone()
    
    def clusterDistribution(self):
        query = "select cluster, count(*) as Total_Stations from water_quality group by cluster order by cluster;"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def hashPassword(self,password):
        return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    
    def verifyPassword(self,password,hashPassword):
        return bcrypt.checkpw(password.encode(),hashPassword.encode())
    
    def checkUsername(self,username):
        self.cursor.execute("select username from admin where username = %s;",(username,))
        return self.cursor.fetchone()
    
    def checkEmail(self,email):
        self.cursor.execute("select email from admin where email = %s;",(email,))
        return self.cursor.fetchone()
    
    def signup(self,fullname,username,email,password):
        query = "insert into admin(fullname,username,email,password) values(%s,%s,%s,%s);"
        hashed_password = self.hashPassword(password)
        self.cursor.execute(query,(fullname,username,email,hashed_password))
        self.connection.commit()
        return True
    
    
    def dashboard_summary(self):
        query = """
        select
        count(*) as total_samples,
        count(distinct state) as total_states,
        count(distinct cluster) AS total_clusters,
        sum(case when pollution_index = -1 then 1 else 0 end) as total_anomalies
        from water_quality;"""
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def dashboard_averages(self):
        query = """
        select
            round(avg(ph), 2) as avg_ph,
            round(avg(do_level), 2) as avg_do,
            round(avg(bod), 2) as avg_bod,
            round(avg(nitrate), 2) as avg_nitrate,
            round(avg(conductivity), 2) as avg_conductivity
        from water_quality;"""
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def pollutionTrend(self):
        query ="""select
        state,
        round(avg(pollution_index), 2) as avg_pollution
        from water_quality
        group by state
        order by avg_pollution desc;"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def cluster_distribution(self):
        query = """
        select
            cluster,
            count(*) as total
        from water_quality
        group by cluster
        order by cluster;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def getStates(self):
        query = """
        select distinct state
        from water_quality
        order by state;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def getClusters(self):
        query = """
        select distinct cluster
        from water_quality
        order by cluster;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def filterRecords(self, state, cluster):
        query = """
        select *
        from water_quality
        where (%s = 'All States' or state = %s)
        and (%s = 'All Clusters' or cluster = %s);
        """
        self.cursor.execute(query, (state, state, cluster, cluster))
        return self.cursor.fetchall()
    
    def searchRecords(self, keyword):
        query = """
        select *
        from water_quality
        where station_name like %s
        or state like %s;
        """
        value = "%" + keyword + "%"
        self.cursor.execute(query, (value, value))
        return self.cursor.fetchall()
    
    def getStates(self):
        query = """
        select distinct state
        from water_quality
        order by state;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def parameterStatistics(self):
        query = """
        select
            round(avg(ph),2) as avg_ph,
            min(ph) as min_ph,
            max(ph) as max_ph,
            round(avg(do_level),2) as avg_do,
            min(do_level) as min_do,
            max(do_level) as max_do,
            round(avg(bod),2) as avg_bod,
            min(bod) as min_bod,
            max(bod) as max_bod,
            round(avg(nitrate),2) as avg_nitrate,
            min(nitrate) as min_nitrate,
            max(nitrate) as max_nitrate,
            round(avg(fluoride),2) as avg_fluoride,
            min(fluoride) as min_fluoride,
            max(fluoride) as max_fluoride,
            round(avg(conductivity),2) as avg_conductivity,
            min(conductivity) as min_conductivity,
            max(conductivity) as max_conductivity
        from water_quality;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()
    

    def topPollutedStates(self):
        query = """
        select
            state,
            round(avg(pollution_index),2) as pollution
        from water_quality
        group by state
        order by pollution desc
        limit 10;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def parameterDistribution(self, parameter):
        allowed = [
            "ph",
            "do_level",
            "bod",
            "nitrate",
            "fluoride",
            "conductivity"
        ]
        if parameter not in allowed:
            return []
        query = f"""
        select
            {parameter}
        from water_quality
        order by {parameter};
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def anomalySummary(self):
        query = """
        select
            count(*) as total,
            sum(case when pollution_index = 1 then 1 else 0 end) as normal,
            sum(case when pollution_index = -1 then 1 else 0 end) as anomaly
        from water_quality;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def anomalyDistribution(self):
        query = """
        select
            sum(case when pollution_index = 1 then 1 else 0 end) as normal,
            sum(case when pollution_index = -1 then 1 else 0 end) as anomaly
        from water_quality;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def modelAccuracy(self):
        return {
            "Random Forest": 94.2,
            "KNN": 90.5
        }