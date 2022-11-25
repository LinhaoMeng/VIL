"# VIAL" 

# For running

you need to install the following in your laptop:

- for backend:
1. conda: for package management

- for frontend:
1. nodejs: runtime environment to run Javascript outside the browser

# prepare data

1. create a folder data folder: /backend/data
2. download MNIST, unzip it and put it under data folder (/backend/data/MNIST/...)


# How to run backend

under VIAL folder:
```
cd backend

conda create --prefix ./envs python=3.8 // create vitual environment (only run this command for the first time)

conda activate ./envs //activate vitual enrironment

conda install --file requirements.txt // install packages(only run this command for the first time)

flask run
```

# How to run frontend

Open another console; 

under VIAL folder:
```
cd frontend

npm install # only run this command for the first time you run the code, after all packages are installed under /node_modules, you don't need to run it again

npm run serve
```
Then open browser as hinted in the console
