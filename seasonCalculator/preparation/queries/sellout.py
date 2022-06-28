SELLOUT_QUERY = f"""
    SELECT CLIENT_SALES.[Date]
          ,CLIENT_SALES.[SKU_lv1] as GroupSapRu
          ,CLIENT_SALES.[AmountWithVat] as SebTotalSellout
          ,CLIENT_SALES.[ClientAmountWithVat] as ClientTotalSellout
          ,CLIENT_SALES.[AmountWithVatOnline] as SebOnlineSellout
          ,CLIENT_SALES.[ClientAmountWithVatOnline] as ClientOnlineSellout
          ,CHAINS.ChainNameEn
          ,SEB_GROUPS.[Product Line] as ProductLine
          ,SEB_GROUPS.[English Groupe] as GroupSapEn
          ,SEB_GROUPS.[Business Unit] as BusinessUnit
        FROM [db_1].[schema_1].[t_1] as CLIENT_SALES
    
        INNER JOIN [db_2].[schema_2].[t_2] AS CHAINS
        ON CLIENT_SALES.[IDChain] = CHAINS.[IDChain]
        INNER JOIN [db_3].[schema_3].[t_3] AS SEB_GROUPS
        ON CLIENT_SALES.SKU_lv1 = SEB_GROUPS.SKU_lv
    
        WHERE datatype = 'W' and year > 2018
"""
