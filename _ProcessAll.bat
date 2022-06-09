::CapturingReality

:: switch off console output
@echo off

setlocal enableDelayedExpansion

call SetVariables.bat

set ImageFolders[0]=IMG_8977
set ImageFolders[1]=IMG_8980
set ImageFolders[2]=IMG_8981
set ImageFolders[3]=IMG_8982
set ImageFolders[4]=IMG_8983
set ImageFolders[5]=IMG_8984
set ImageFolders[6]=IMG_8985
set ImageFolders[7]=IMG_8986
set ImageFolders[8]=IMG_8988
set ImageFolders[9]=IMG_8992
set ImageFolders[10]=IMG_8994
set ImageFolders[11]=IMG_8995
set ImageFolders[12]=IMG_8997
set ImageFolders[13]=IMG_9001
set ImageFolders[14]=IMG_9004
set ImageFolders[15]=IMG_9005
set ImageFolders[16]=IMG_9006
set ImageFolders[17]=IMG_9007
set ImageFolders[18]=IMG_9009
:: root path to work folders where all the datasets are stored (%~dp0 means the flder in which this script is stored)

set RootFolder=C:\Users\roncl\Documents\FaitMaison\AutoReconstruction\Images

for %%a in (3,4,5,6,7,8,9,10,11,12,13,16,18) do (

:: variable storing path to images for creating model
set Images=%RootFolder%\!ImageFolders[%%a]!

echo !Images!
mkdir !Images!\project

:: set a new name for calculated model
:: set ModelName="model_rc"

:: set the path, where model is going to be saved, and its name
set Model=!Images!\project\model_rc.obj

:: variable storing path to images for texturing model
set Project=!Images!\project\model_rc.rcproj

:: Variable storing a name of file with parameters for automatic markers detection in RC.
set DetectMarkersParams=C:\Users\roncl\Documents\FaitMaison\AutoReconstruction\DetectMarkersParams.xml

:: run RealityCapture
%RealityCaptureExe% -addFolder !Images! ^
        -getLicense "5678"^
        -detectMarkers %DetectMarkersParams% ^
        -align ^
        -setReconstructionRegionAuto ^
        -calculateNormalModel ^
        -selectMarginalTriangles ^
        -removeSelectedTriangles ^
        -renameSelectedModel "model_rc" ^
        -calculateTexture ^
        -save !Project! ^
        -exportModel "model_rc" !Model! ^
        -quit
)