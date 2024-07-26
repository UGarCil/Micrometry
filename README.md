# Micrometry
This is a simple interface aimed to provide an efficient measurement tool for microscopy, and other applications that require the mapping of pixels into units of measurement.

![Length of a Rotifer using Bezier curves](https://raw.githubusercontent.com/UGarCil/Micrometry/main/Examples/rotifer_0d1mm.png)

![An edge and motion detection tool](https://github.com/UGarCil/Micrometry/blob/main/Examples/demo2.gif?raw=true)

![A GUI for quick measurement taking](https://github.com/UGarCil/Micrometry/blob/main/Examples/gifDemo.gif?raw=true)

## INSTALLATION

You will need a version of python >=3.6 with the following libraries installed:  
&emsp; pygame 2.1.2  
&emsp; opencv 4.6.0

I recommend the use of a virtual environment. For a commercial laptop, a good choice is to use Anaconda. Install anaconda for your OS and follow the next steps:  

1. Clone the repository to your computer
2. Open Terminal OR the Anaconda Prompt, and navigate to the folder Micrometry (if you didn't add Anaconda to the path variables; open Anaconda Prompt if not sure and navigate to the folder Micrometry)
3. Run 
    
```
    conda env create -f requirements.yaml
```
4. Once the new environment has been created, you can type 
```
    conda activate micrometry-env
```
5. Now you can open the program by using entering the measure_curves or measure_lines folder, then execute the python script:  
```
    cd measure_curves
    python main.py --ci 0
```

# TUTORIALS
- How to use Micrometry:   https://www.youtube.com/watch?v=fBV8OwCvHgQ&t=535s&ab_channel=SiliconHeart
- Micrometry Datasets:  https://youtu.be/RYkdiLIK-GM

# DOCUMENTATION
You can find targeted tutorials for each submodule, and additional information in the official online docs at https://ugarcil.github.io/Micrometry/