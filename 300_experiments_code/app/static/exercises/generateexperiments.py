import random
import os

directory = "."

heading = """<html>

<head>
</head>

<body>
  <p style = "margin-left :1em">

"""

footing = """
  <p>
</body>

</html>"""


for i in range(0,100):
    os.mkdir(str(i))
    with open(directory + "/%d/regulation_%d.html"%(i, i), "w") as file:
        asset1, asset2, asset3 = [random.uniform(0,2) for i in range(3)]
        file.write(heading)
        file.write("    <br> asset1 weight is %.2f \n \n"%(asset1))
        file.write("    <br> asset2 weight is %.2f \n \n"%(asset2))
        file.write("    <br> asset3 weight is %.2f \n"%(asset3))
        file.write(footing)
        file.close()



    with open(directory + "/%d/balancesheet_%d.html"%(i, i), "w") as file:
        asset1, asset2, asset3 = [random.randrange(1000,10000) for i in range(3)]
        file.write(heading)
        file.write("    <br> %d € of asset 1 \n \n"%(asset1))
        file.write("    <br> %d € of asset 2 \n \n"%(asset2))
        file.write("    <br> %d € of asset 3 \n"%(asset3))
        file.write(footing)
        file.close()
