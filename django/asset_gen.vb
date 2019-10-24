Sub GenHier(limit As Integer)
    Dim genArr, writeArr, maxlvl
    ReDim genArr(1 To limit, 1 To 4)
    ReDim writeArr(1 To limit, 1 To 11)
    maxlvl = 4
    genArr(1, 1) = "SITE"
    genArr(1, 2) = "SITE TOP LEVEL ENTRY"
    genArr(1, 3) = "SITE"
    genArr(1, 4) = 0
    For i = 2 To limit
        genArr(i, 1) = "SITE-ROLE-NUM-" & i - 1
        genArr(i, 2) = "Asset Number " & i - 1 & " Name"
        genArr(i, 3) = "Location " & i - 1
        genArr(i, 4) = Round(maxlvl * Rnd + 1, 0)
    Next i
    For i = limit To 1 Step -1
        writeArr(i, 1) = genArr(i, 1) 'id
        writeArr(i, 2) = genArr(i, 2) 'aenm
        writeArr(i, 3) = "SITE"
        writeArr(i, 5) = "Asset"
        writeArr(i, 6) = "Asset"
        writeArr(i, 7) = 1
        writeArr(i, 8) = genArr(i, 3) 'entloc
        writeArr(i, 9) = 1
        For j = i - 1 To 1 Step -1
            If genArr(j, 4) < genArr(i, 4) Then
                writeArr(i, 4) = genArr(j, 1)
                j = 0
            End If
        Next j
    Next i
    Sheet1.Range(Sheet1.Cells(1, 1), Sheet1.Cells(limit, 9)).Value2 = writeArr
    Debug.Print ("done")
End Sub
