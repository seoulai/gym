class AgentInfo():
    def __init__(
        self,
    ):
        self.cash = 100000000
        self.asset_qtys = {"KRW-BTC":0}

# class DBClient():
# 	def __init__(self,host="127.0.0.1",port=,userid="",password="",database=""):
# 		self.conn = mysql.connector.connect(host=host,port=port,user=userid,password=password,database=database)
# 		self.cursor = self.conn.cursor()
# 
# 	def getCurrentDateTime(self):
# 		return time.strftime("%Y%m%d%H%M%S")
# 
# 	def query(self,qry):
# 		self.cursor.execute(qry)
# 		rows = self.cursor.fetchall()
# 		return rows
# 
# 	def execute(self,qry,commit=False):
# 		self.cursor.execute(qry)
# 		
# 		if commit:
# 			self.conn.commit()
# 
# 	def commit(self):
# 		self.conn.commit()
# 
# 
# 	def runQuery(self,qry):
# 		df = pd.read_sql(qry,self.conn)
# 		return df
# 		
# 
# 	def convertStockCodesToArray(self,rows,with_name):
# 		stock_codes = []
# 		for a_row in rows:
# 			if a_row[0]:
# 				if with_name:    #stock_name을 붙이고 싶은 경우.
# 					stock_codes.append( (a_row[0],a_row[1]) )
# 				else:
# 					stock_codes.append(a_row[0])
# 
# 		#logging.info(stock_codes)
# 		return stock_codes
# 
# 
# 	def getStockCode(self,market_type,limit=10000,with_name=False, stock_code='000000'):		
# 		sql = "select stock_code,stock_name from stock_code_data "
# 		if market_type==MARKET_ALL:
# 			sql += "where (market_type=%s or market_type=%s) " % (MARKET_KOSDAQ,MARKET_KOSPI)	#and stock_code >= '009970'
# 		else:
# 			sql += "where market_type=%s" % (market_type)
# 
# 		sql += " and   stock_section = 1 "   #주권만 고려함. 외국주권, 주식예탁증서는 고려하지 않음. (section type 13, 6)
# 		sql += " and   stock_status = 0 "    #주식상태가 정상.	
# 		sql += " and   spac_yn = 'N' "       #스팩 아님.
# 		sql += " and   stock_code >= '%s' " % (stock_code)
# 		#sql += " and   stock_code >= '024800' "
# 		#sql += " and   stock_code IN( '035420', '237690', '071055') "
# 		sql += " limit %s" % (limit)
# 		rows = self.query(sql)
# 
# 		return self.convertStockCodesToArray(rows,with_name)
# 
# 	def getDataCountWithinRange(self,table,stock_code,start_date,end_date):
# 		sql = "select count(*) from %s where stock_code='%s' " % (table,stock_code)
# 
# 		sql += " and trade_datetime between '%s' and '%s'" % (start_date,end_date)
# 		rows = self.query(sql)
# 		return rows[0][0]
# 
# 	def getCybosGroup(self, bass_dt):		
# 		sql  = "select '%s' as bass_dt, c.industry_code as industry_code, c.industry_name as industry_name, count(*) as cnt " % (bass_dt)
# 		sql += "     , round(avg(b.pbr), 3) as avg_pbr "
# 		sql += "     , round(avg(b.per), 3) as avg_per "
# 		sql += "     , round(avg(b.psr), 3) as avg_psr "
# 		sql += "     , round(avg(b.pcr), 3) as avg_pcr "
# 		sql += "     , round(avg(b.bps), 3) as avg_bps "
# 		sql += "     , round(avg(b.eps), 3) as avg_eps "
# 		sql += "     , round(avg(b.roe), 3) as avg_roe "
# 		sql += "     , round(avg(b.dept_ratio), 3) as avg_dept_ratio "
# 		sql += "	 , round(avg(b.net_income_growth_ratio), 3) as avg_net_income_growth_ratio "
# 		sql += "     , round(avg(b.q_bps), 3) as avg_q_bps "
# 		sql += "     , round(avg(b.q_roe), 3) as avg_q_roe "
# 		sql += "     , round(avg(q_dept_ratio), 3) as avg_q_dept_ratio "
# 		sql += "     , round(avg(q_net_income_growth_ratio), 3) as avg_q_net_income_growth_ratio      "
# 		sql += "     , round(stddev(b.pbr), 3) as std_pbr "
# 		sql += "     , round(stddev(b.per), 3) as std_per "
# 		sql += "     , round(stddev(b.psr), 3) as std_psr "
# 		sql += "     , round(stddev(b.pcr), 3) as std_pcr "
# 		sql += "     , round(stddev(b.bps), 3) as std_bps "
# 		sql += "     , round(stddev(b.eps), 3) as std_eps "
# 		sql += "     , round(stddev(b.roe), 3) as std_roe "
# 		sql += "     , round(stddev(b.dept_ratio), 3) as std_dept_ratio "
# 		sql += "	 , round(stddev(b.net_income_growth_ratio), 3) as std_net_income_growth_ratio "
# 		sql += "     , round(stddev(b.q_bps), 3) as std_q_bps "
# 		sql += "     , round(stddev(b.q_roe), 3) as std_q_roe "
# 		sql += "     , round(stddev(q_dept_ratio), 3) as std_q_dept_ratio "
# 		sql += "     , round(stddev(q_net_income_growth_ratio), 3) as std_q_net_income_growth_ratio "
# 		sql += "from (select stock_code, stock_name, close_price, sttl_dt, quater_dt, round(close_price/bps, 2) AS pbr, per, round(close_price/sps, 2) AS psr, round(close_price/cfps, 2) AS pcr, bps, eps, roe "
# 		sql += ", dept_ratio, net_income_growth_ratio, q_bps, q_roe, q_dept_ratio, q_net_income_growth_ratio "
# 		sql += "from cybos_indicator a "
# 		sql += "where a.bass_dt = '%s' " % (bass_dt)
# 		sql += "and   right(a.stock_code, 1) = '0'  "
# 		sql += "and   per <> 0) b "
# 		sql += "   , stock_code_data c "
# 		sql += "where b.stock_code = c.stock_code "
# 		sql += "group by c.industry_code, c.industry_name "
# 		df = pd.read_sql(sql, self.conn)
# 		return df
