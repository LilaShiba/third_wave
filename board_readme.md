# Raspberry Pi 5 Setup Guide 🚀

This guide demonstrates the following: creating a virtual environment, cloning a repository,  installing its dependencies, and debugging hardware on the RPI 5.


## Navigation Table ❤️🔥⚡

- **Main Landing Page** ❤️✨: [Readme.md](https://github.com/LilaShiba/third_wave/blob/main/readme.md)
- **RPI Board** ⚡: [RPI Documentation](https://github.com/LilaShiba/third_wave/blob/main/board_readme.md)
- **OS Choice** 🌟: [os.md](https://github.com/LilaShiba/third_wave/blob/main/os.md)

## Prerequisites 📋

Ensure your OS is up to date. Many fixes came in January 2024:

<pre><code>
sudo apt-get update
sudo apt-get upgrade
</code></pre>

## Installation Steps 🛠

### 1. Install Git and Python 🐍

Now, install Git and Python3, along with the `venv` module to manage virtual environments.

<pre><code>sudo apt-get install -y git python3 python3-venv
</code></pre>

### 2. Set Up Virtual Environment 🌐

Create a directory for your project and navigate into it:

<pre><code>mkdir my_project
cd my_project
</code></pre>

Create a virtual environment named `my_env_name`:

<pre><code>python3 -m venv my_env_name
</code></pre>

Activate the virtual environment:

<pre><code>source my_env_name/bin/activate
</code></pre>

This step will ensure compatibility and preserve your devices Python env.

### 3. Clone the Repository 📦

<pre><code>git clone https://github.com/LilaShiba/flask_server_ubi.git
</code></pre>

Navigate into the cloned repository:

<pre><code>cd flask_server_ubi
</code></pre>

### 4. Install Dependencies 📚

Located in `requirements.txt`:

<pre><code>pip install -r requirements.txt
</code></pre>

#### Enable I2C communication

Open the pi terminal and run 

<pre><code>sudo raspi-config </code></pre>

This will open the option menu. You will want to select Interface Options, and then enable I2C.

## Running the Application 🚀



To run the Hardware:

<pre><code>python app/utils/main.py
</code></pre>

## Debugging
The I2C pins can be a bit tricky. First, we will install some tools to help peak inside the RPI. Then we will look at the states of the GPIO. Lastly, we will scan the I2C bus for any devices on said port. 

Update i2c-tools
<pre><code>
 sudo apt update
 sudo apt install -y i2c-tools

</code></pre>

Check the GPIO pins
If the sda and scl pins are reading high, your sensors are not detected and may be damaged.

<pre><code>gpio readall
</code></pre>

Find devices on I2C bus. This command will give you the address for all I2C devices
<pre><code>i2cdetect -y 1
</code></pre>
