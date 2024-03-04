# 🧙‍♂️✨RPi 5 OS Choice ✨🧙‍♂️

After research and experimentation with Raspbian, Ubuntu, and Fedora, Fedora IoT was selected for its lightweight and high reliability ratio. Raspbian presented many issues interfacing with I2C. Ubuntu was too clunky. FIoT was just right 🌟

Documentation for Raspbian is provided as it is only a matter of time before they fix these errors, mainly the remapping of the gpio module to rpi5s new structure.


## Navigation Table ❤️🔥⚡

| Document Title              | Link                                                                                      |
|-----------------------------|-------------------------------------------------------------------------------------------|
| **Main Landing Page** ❤️✨  | [Readme.md](https://github.com/LilaShiba/flask_server_ubi/blob/main/readme.md)            |
| **Sensor Setup Guide** 🔥   | [build_instructions.md](https://github.com/LilaShiba/flask_server_ubi/blob/main/build_instructions.md) |
| **RPI Server Documentation**⚡| [RPI Server Documentation](https://github.com/LilaShiba/flask_server_ubi/blob/main/board_readme.md)    |
| **OS Choice** 🌟            | [os.md](https://github.com/LilaShiba/flask_server_ubi/blob/main/os.md)                    |






## 🚀 Getting Started
The front-end work of setting up the OS for SSH is documented below and worth the trouble. Raspbian and RPi Baker offer wonderful options to install the OS with SSH and Wi-Fi pre-configured, streamlining the setup and start-time. However, the I2C errors proved to outweigh this benefit 🛠.

### 📦 Download Fedora IoT
- Go to Fedora IoT [download page](https://getfedora.org/en/iot/download/).
- Grab the ARM image for RPi5.

### 💾 Flash SD Card
- Use [Balena Etcher](https://www.balena.io/etcher/) or similar.
- Flash the Fedora IoT image to your SD card.

### 🥾 Boot Up
- Insert SD into RPi5.
- Connect to monitor and power up.

## 🛠 Setup

### 🌐 Configure Network
<pre><code>nmtui-connect
</code></pre>

### 🔄 Update System
<pre><code>sudo dnf update
</code></pre>

## 🔐 SSH Magic

### 🧙‍♂️ Check SSH Status
<pre><code>systemctl status sshd
</code></pre>

### 📦 Install SSH (if needed)
<pre><code>sudo dnf install openssh-server
</code></pre>

### 🚀 Enable SSH
<pre><code>sudo systemctl enable --now sshd
</code></pre>

### 🛡 Firewall Config
<pre><code>sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
</code></pre>

## 🌈 Connect via SSH

### 🕵️‍♂️ Find Pi's IP
<pre><code>hostname -I
</code></pre>

### 🚪 SSH In
<pre><code>ssh fedora@your_rpi_ip
</code></pre>

### 🔑 Change Default Password
<pre><code>passwd
</code></pre>

## ✨ Voilà! Your RPi5 is now a Fedora IoT server with SSH ✨
