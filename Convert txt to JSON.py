import json
import csv

# See link for reference: http://www.askyb.com/python/converting-tab-delimited-textfile-to-json/


# save the json output as emp.json 
jsfile = open('movies.json', 'w', encoding='utf8')
jsfile.write('[\r\n')
 
with open('Movie Dataset for Machine Learning.txt','r', encoding='utf8') as f:
    next(f) # skip headings
    reader=csv.reader(f,delimiter='\t')
 
    # get the total number of rows excluded the heading
    row_count = len(list(reader))
    ite = 0
 
    # back to first position
    f.seek(0)
    next(f) # skip headings
    
    for budget,rating,month,classif,title,pratio,genres in reader:
 
        ite+= 1
        
        jsfile.write('\t{\r\n')
        
        b_w = '\t\t\"budget\": \"' + budget + '\",\r\n'
        r_w = '\t\t\"rating\": \"' + rating + '\",\r\n'
        m_w = '\t\t\"month\": \"' + month + '\",\r\n'
        c_w = '\t\t\"class\": \"' + classif + '\",\r\n'
        t_w = '\t\t\"title\": \"' + title + '\",\r\n'
        p_w = '\t\t\"pratio\": \"' + pratio + '\",\r\n'
        g_w = '\t\t\"genres\": \"' + genres + '\"\r\n'
       
        jsfile.write(b_w)
        jsfile.write(r_w)
        jsfile.write(m_w)
        jsfile.write(c_w)
        jsfile.write(t_w)
        jsfile.write(p_w)
        jsfile.write(g_w)
 
        jsfile.write('\t}')
 
        # omit comma for last row item
        if ite < row_count:
            jsfile.write(',\r\n')
 
        jsfile.write('\r\n')
 
jsfile.write(']')
jsfile.close()
