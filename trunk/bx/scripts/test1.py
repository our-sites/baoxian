#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/14.
# ---------------------------------
import  urllib2

a='''<div>
			<p>　　新疆将支持商业<a href="http://insurance.hexun.com/" target="_blank">保险</a>机构承办<a href="http://www.fangxinbao.com/baoxian/zhongjixian/" target="_blank">大病保险</a>，通过政府招标选定商业保险机构。符合保险监管部门基本准入条件的商业保险机构自愿参加投标，合同期限原则上不低于3年。</p><p>　　新疆日前出台《关于全面实施城乡居民大病保险工作的意见》，进一步完善城乡居民基本医疗保障制度。意见明确，自治区将支持商业保险机构承办大病保险。自治区人力资源和社会保障、财政、卫生计生、保监部门共同制定大病保险的筹资、支付范围、最低支付比例以及就医、结算管理等基本政策。原则上通过政府招标选定商业保险机构承办大病保险业务，在正常招标不能确定承办机构的情况下，由各地明确承办机构的产生办法。商业保险机构承办大病保险的<a href="http://www.fangxinbao.com/feiLv/zhongjixian/" target="_blank">保费</a>收入，执行现行国家税收优惠政策。</p><p>　　招标主要包括具体支付比例、盈亏率、配备的承办和管理力量等内容。符合保险监管部门基本准入条件的商业保险机构自愿参加投标。招标人应当与中标的商业保险机构签署保险合同，明确双方责任、权利和义务，合同期限原则上不低于3年。因违反合同约定，或发生其他严重损害参保人权益的情况，可按照约定提前终止或解除合同，并依法追究责任。</p><p>　　同时要求，商业保险机构承办大病保险获得的保费实行单独核算，确保资金安全和偿付能力。商业保险机构要建立专业队伍，为参保人提供更加高效便捷的服务。发挥商业保险机构全国网络优势，简化报销手续，推动异地医保即时结算。</p><p>　　此外，大病保险实行地（州、市）级统筹，全区展开，为自治区统筹创造条件。统筹地区要做到筹资标准、待遇水平、招标、保险公司、资金管理五统一。</p><p>　　据了解，大病保险保障对象为城乡居民基本医保参保人，保障范围与城乡居民基本医保相衔接，可将临床疗效确切但<a href="http://www.fangxinbao.com/feiLv/zhongjixian/" target="_blank">价格</a>昂贵的特殊药品和诊疗服务项目逐步纳入大病保险支付范围。参保人患大病发生高额医疗费，由大病保险对经城乡居民基本医保按规定支付后个人负担的合规医疗费用给予保障。保障水平按医疗费用高低分段制定大病保险支付比例，医疗费用越高支付比例越高。2016年大病保险支付比例应达到50%以上，之后进一步提高支付比例。</p>&#13;
			&#13;
			<div style="text-align:right;font-size:12px">（责任编辑： HN666）</div>&#13;
			&#13;</div>
'''
import  pyquery
b=pyquery.PyQuery(a)
print b("a")
import  urllib2
import  urllib
import  requests
data=requests.post("http://iir.circ.gov.cn/web/baoxyx!searchInfoBaoxyx.html",{"id_card":"","certificate_code":"","evelop_code":"02000235020080002011002289",
                                                                              "name":"","valCode":""})
doc=pyquery.PyQuery(data.content.decode("gbk"))
print doc
print doc(".xxxx_title")