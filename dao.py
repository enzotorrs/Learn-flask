import psycopg2

conect = psycopg2.connect(host='192.168.0.136', database='Site',
                                        user='enzotorr',
                                        password='cueca135galinha')
cursor = conect.cursor()


