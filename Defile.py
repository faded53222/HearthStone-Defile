import csv
import pandas as pd
import itertools as it
import copy
import pickle
class tuple_with_sum:
	def __init__(self,tuple1):
		self.tuple1=tuple1
		sum1=0
		max1=0
		for i in tuple1:
			sum1+=i.attack
			if i.attack>max1:
				max1=i.attack
		self.sumi1=sum1
		self.sumi2=sum1-max1
class minion:
	def __init__(self,attack,health,name,ID,ability):
		self.attack=attack
		self.health=health
		self.name=name
		self.ID=ID
		self.ability=[]
		if isinstance(ability,str):
			self.ability=ability.split(',')
		if attack==0:
			self.able_to_attack=0
		else:
			self.able_to_attack=1
			if "windfury" in self.ability:
				self.able_to_attack+=1
	def copy_constructor(self,another):
		self.attack=another.attack
		self.health=another.health
		self.name=another.name
		self.able_to_attack=another.able_to_attack
	def show(self):
		print("name:"+self.name)
		print("attack: "+str(self.attack))
		print("health: "+str(self.health))
		print("ID: "+str(self.ID))
	def attacki(self,another):
		self.health-=another.attack
		another.health-=self.attack
		self.able_to_attack-=1
user_minion_list=[]
enemy_minion_list=[]
NN=0
def load(file_name):
	f=open(file_name)
	data=pd.read_csv(f)
	NN=len(data)
	for i in range(len(data)):
		line=data.loc[i]
		attack=line.attack
		health=line.health
		name=line.Name
		belong=line.belong
		ability=line.ability
		new_minion=minion(attack,health,name,i,ability)
		if(belong=="user"):
			user_minion_list.append(new_minion)
		else:
			enemy_minion_list.append(new_minion)
def get_sum_of_attack():
	for i in enemy_minion_list:
		if 'taunt' in i.ability:
			return 0
	sumi=0
	for j in user_minion_list:
		sumi+=j.attack*j.able_to_attack
	return sumi 
user_minion_status_keep=[]
enemy_minion_status_keep=[]
def save_status():
	user_minion_status_keep.append(pickle.dumps(user_minion_list))
	enemy_minion_status_keep.append(pickle.dumps(enemy_minion_list))
def load_status():
	global user_minion_list
	global enemy_minion_list
	user_minion_list=pickle.loads(user_minion_status_keep[-1])
	enemy_minion_list=pickle.loads(enemy_minion_status_keep[-1])
def pop_status():
	user_minion_status_keep.pop()
	enemy_minion_status_keep.pop()
def funeral():
	for i in user_minion_list+enemy_minion_list:
		if i.health<=0:
			if i in user_minion_list:
				user_minion_list.remove(i)
			if i in enemy_minion_list:
				enemy_minion_list.remove(i)
def health_exist_n(n):
	for i in user_minion_list+enemy_minion_list:
		if i.health==n:
			return 1
	return 0
def judge_success(tragedy):
	maxi=0
	maxi_enemy=0
	count=0
	dic_health={}
	for i in range(1,30):
		dic_health[i]=0
	for i in user_minion_list+enemy_minion_list:
		dic_health[i.health]+=1
		if dic_health[i.health]==1:
			count+=1
		if i.health>maxi:
			maxi=i.health
		if i in enemy_minion_list:
			if i.health>maxi_enemy:
				maxi_enemy=i.health
	if tragedy==1:
		if count==maxi:
			return 1
	if tragedy!=1:
		for i in range(1,maxi_enemy):
			if dic_health[i]==0:
				return 0
		return 1
	return 0
def get_all_choices_to_make_up_n(n,tragedy):
	user_minion_list_can_attack=[]
	for i in user_minion_list:
		if i.able_to_attack>=1:
			user_minion_list_can_attack.append(i)
	all_choices=[]
	lab=0
	for enemy in enemy_minion_list:
		if 'taunt' in enemy.ability:
			lab=1
			break
	enemy_minion_list_can_be_attacked=[]		
	if lab==0:
		enemy_minion_list_can_be_attacked=enemy_minion_list
	if lab==1:
		for enemy in enemy_minion_list:
			if 'taunt' in enemy.ability:
				enemy_minion_list_can_be_attacked.append(enemy)

	all_tuple=[]
	for i in range(1,len(user_minion_list_can_attack)+1):
		for one_tuple in list(it.combinations(user_minion_list_can_attack,r=i)):
			new_tuple_with_sum=tuple_with_sum(one_tuple)
			all_tuple.append(new_tuple_with_sum)
	all_tuple.sort(key=lambda b: b.sumi1)
	make_up_list=[]
	make_up_list.append(n)
	if n==1 and lab==1:
		make_up_list.append(0)
	for N in make_up_list:
		for i in user_minion_list_can_attack:
			for j in enemy_minion_list_can_be_attacked:
				if j.attack!=0:
					if (N==0 and i.health-j.attack<0) or i.health-j.attack==N:
						one_choice=((i.ID,),j.ID)
						if one_choice not in all_choices:
							all_choices.append(one_choice)
		for i in enemy_minion_list_can_be_attacked:
			for j in all_tuple:
				if N!=0 and j.sumi1+N>i.health:
					break
				if (N==0 and i.health>j.sumi2 and i.health<j.sumi1) or j.sumi1+N==i.health:
					ID_tuple=()
					for a in j.tuple1:
						ID_tuple+=(a.ID,)
					one_choice=(ID_tuple,i.ID)
					if one_choice not in all_choices:
						all_choices.append(one_choice)
	return all_choices
one_possible_way=[]
possible_ways=[]
poppy=[]
possible_way_keep1=[]
max_sum_of_attack=0
def deal(n,tragedy):
	global max_sum_of_attack
	global possible_way_keep1
	if health_exist_n(n) or n==0:
		poppy.append(0)
		deal(n+1,tragedy)
	all_choices=get_all_choices_to_make_up_n(n,tragedy)
	if len(all_choices)==0:
		success_or_not=judge_success(tragedy)
		if success_or_not ==1:
			if poppy[-1]==1:
				if not one_possible_way in possible_ways:
					possible_ways.append(one_possible_way.copy())
					if tragedy==2:
						sum_of_attack=get_sum_of_attack()
						if(sum_of_attack>max_sum_of_attack):
							max_sum_of_attack=sum_of_attack
							possible_way_keep1=one_possible_way.copy()
						
		if poppy[-1]==1:
			one_possible_way.pop()
		poppy.pop()
		return
	save_status()
	for one_way_ID in all_choices:
		one_step=[]
		load_status()	
		ID_dic={}
		for thing in user_minion_list+enemy_minion_list:
			ID_dic[thing.ID]=thing
		attacked=ID_dic[one_way_ID[1]]
		for one_attacker_ID in one_way_ID[0]:
			one_attacker=ID_dic[one_attacker_ID]
			one_attacker.attacki(attacked)
			one_step.append(one_attacker.name+" ##attack## "+attacked.name)
		one_possible_way.append(one_step)
		funeral()
		poppy.append(1)
		deal(n,tragedy)
	load_status()	
	pop_status()
	if poppy[-1]==1:
		one_possible_way.pop()
	poppy.pop()
	return	
if __name__ == "__main__":
	tragedy=2
	#adjust this line to get your ideal result
	#when tragedy==1 all minions ,including yours, would be destroyed
	#when tragedy==2 only enemy minions would be destoryed.
	#    and a way that will deal the highest damage to enemy hero would be taken out 
	deal_file_name="minions.csv"
	load(deal_file_name)
	if tragedy==1:
		save_file_name="result1.txt"
	if tragedy==2:
		save_file_name="result2.txt"
	poppy.append(0)
	deal(1,tragedy)
	#If you have plenty of time or you can't get a result when using deal(1,tragedy) ,
	#you may use deal(0,tragedy)
	#Because there are too many ways to get a minion's health to or under 0.
	#if you make up number from 0,it would cost a lot of time.
	#Using deal(1,tragedy),you will get less cases when using tragedy 1
	#and your result would be a little less accurate when using tragedy 2
	#But it's worth it.
	f=open(save_file_name,'w')
	for one_way in possible_ways:
		f.write(str(one_way)+'\n')
		#print(one_way)
		#print("\n")
	f.close()
	if tragedy==2:
		print("to_get_highest damage")
		print(possible_way_keep1)
		print("highest_damage_is: "+str(max_sum_of_attack))
