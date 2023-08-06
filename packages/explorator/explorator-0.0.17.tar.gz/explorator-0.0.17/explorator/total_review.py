import pandas as pd


def write_reports_view_to_one_excel(reports, report_name):
    #report_name='! rr.xlsx'
    writer = pd.ExcelWriter(r'' + report_name, engine='xlsxwriter')
    workbook = writer.book
    int_format = workbook.add_format({'num_format':'# ### ### ##0'})
    float_format = workbook.add_format({'num_format':'# ### ### ##0.00'})
    percent_format = workbook.add_format({'num_format':'0%'})

    g_sheetname =  'general'
    rep_to_xl = pd.DataFrame()
    
    for rep in reports.keys(): #files_ok:
        rep_i = reports[rep]
        rep_i['file'] = rep
        rep_to_xl = rep_to_xl.append(rep_i)
    
    
    rep_to_xl[['file', 'general info', 'value','count', 'describe', 'examples']].to_excel(writer, g_sheetname, startcol = 0)
    worksheet = writer.sheets[g_sheetname]
        
    for letter in ['D','E','G','N','O','P','Q','R','W','X','Y']:
        worksheet.set_column('{0}:{0}'.format(letter), None, int_format)

    for letter in ['S', 'T','U','V']:
        worksheet.set_column('{0}:{0}'.format(letter), None, float_format)

    for letter in ['F', 'H']:
        worksheet.set_column('{0}:{0}'.format(letter), None, percent_format)


    #df_gen.to_excel(writer, g_sheetname)
    #worksheet = writer.sheets[g_sheetname]

    writer.save()