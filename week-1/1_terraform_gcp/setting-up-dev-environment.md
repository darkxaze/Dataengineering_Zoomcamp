
# Setting up the development environment on Google Virtual Machine

## Data Engineering Zoom Camp 2023

**Aditya Gupta** · Mar 6, 2023 · 7 min read

## Table of contents

- [Configure SSH Keys](#configure-ssh-keys)
- [Create a Virtual Machine](#create-a-virtual-machine)
- [Configure the Virtual Machine](#configure-the-virtual-machine)
  - [Installing Anaconda](#installing-anaconda)
  - [Installing Docker](#installing-docker)
  - [Installing docker-compose](#installing-docker-compose)
  - [Installing Pgcli](#installing-pgcli)
  - [Installing Terraform](#installing-terraform)
  - [Creating a service account](#creating-a-service-account)
  - [Authenticate GCP using the service account credentials](#authenticate-gcp-using-the-service-account-credentials)
  - [Installing Pyspark](#installing-pyspark)
  - [Cloning the course repo](#cloning-the-course-repo)
  - [Open a Remote Connection from Visual Studio Code](#open-a-remote-connection-from-visual-studio-code)
- [Conclusion](#conclusion)

I'm participating in this year's cohort of the [Data Engineering Zoomcamp 2023](https://github.com/DataTalksClub/data-engineering-zoomcamp). This is a community-led, free data engineering course of about 8 weeks. In this blog, I'll summarise the steps to configure a Google Virtual Machine to make it ready for the rest of the course.

## Configure SSH Keys

Generate a new SSH key with the following commands:

```bash
cd ~/.ssh
ssh-keygen -t rsa -f <key-file-name> -C <username> -b 2048
```

It'll raise a prompt to enter a passphrase. You can leave it and press `enter`. If it asks for confirmation, press `enter` again.

This generates 2 files in the .ssh folder, one for the public (`gcp-blog.pub`) and one for the private key (`gcp-blog`).

Next, upload the public key to GCP with the following steps:

- Open the `gcp-blog.pub` file and copy its contents. Or you can use the `cat` command to display the contents in the terminal.

- Go to the Google Cloud console > Compute Engine > Settings > Metadata.

- Click on SSH Keys > Add SSH Keys

- Paste the contents of the public key that you copied previously on the text box and click Save.

Now, you can connect to your Google VMs using the following command:

```bash
ssh -i <PATH_TO_PRIVATE_KEY> <USERNAME>@<EXTERNAL_IP>
```

## Create a Virtual Machine

To set up a Virtual Machine:

- Go to Compute Engine > VM Instances

- Click on Create Instance.

- Populate the configurations for the VM with the following details (Name and Region can be as per your preference):

- Next, change the boot disk with the following configurations:

- Leave the rest of the configurations to default values and click Create.

This will spin up a virtual machine instance for you. In order to ssh into this instance, run the following command:

```bash
ssh -i <PATH_TO_PRIVATE_KEY> <USERNAME>@<EXTERNAL_IP>
```

Here's an example on my system:

You can also configure an ssh alias, which is a convenient way to store the ssh details in a config file. You can follow my blog on this and set up your alias to easily connect with a VM.

[https://itsadityagupta.hashnode.dev/ssh-simplified-aliasing-credentials-with-config-files](https://itsadityagupta.hashnode.dev/ssh-simplified-aliasing-credentials-with-config-files)

I have created an alias for the VM by the name `dezoomcamp`. Here's the new command to ssh:

```bash
ssh dezoomcamp
```

> If you want to connect to a VM using any other options, please go through the official documentation on [Connecting to VMs](https://cloud.google.com/compute/docs/instances/connecting-to-instance).

## Configure the Virtual Machine

Now that you have a Virtual Machine running and a way to ssh into it and run Linux commands, let's start with installing the requirements of the course to make it ready for development.

### Installing Anaconda

- Visit [Anaconda's website](https://www.anaconda.com) and copy the link to Linux 64-Bit Installer.

- Download the file in the VM:

  ```bash
  wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
  ```

- Run the downloaded file:

  ```bash
  bash Anaconda3-2022.10-Linux-x86_64.sh
  ```

- Keep pressing Enter to scroll down and enter `yes` to accept the license terms.

- Press Enter to confirm the default location.

- Enter `yes` to run the `conda init` when asked.

- After the installation is complete, run the command `source .bashrc` to apply the changes to the `.bashrc` file. Alternatively, you can log out of the session using the `logout` command and then ssh back in for the changes to take effect.

You'll notice the anaconda environment name in the shell prompt once the changes are applied. Also, from the above image it is confirmed that python is also installed.

### Installing Docker

Run the following commands:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install docker.io
```

This will install docker but you'll not be able to run it without `sudo`. To run docker without `sudo`, add your username to the docker group:

```bash
sudo usermod -aG docker $USER
```

Log out and log back in for the changes to take effect.

Verify the installation by running:

```bash
docker --version
```

### Installing docker-compose

Download the latest version of docker-compose:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Apply executable permissions to the binary:

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

Verify the installation:

```bash
docker-compose --version
```

### Installing Pgcli

Pgcli is a command-line interface for PostgreSQL with auto-completion and syntax highlighting.

Install pgcli using pip:

```bash
pip install pgcli
```

Verify the installation:

```bash
pgcli --version
```

### Installing Terraform

Download the latest version of Terraform:

```bash
wget https://releases.hashicorp.com/terraform/1.1.7/terraform_1.1.7_linux_amd64.zip
```

Unzip the downloaded file:

```bash
unzip terraform_1.1.7_linux_amd64.zip
```

Move the binary to `/usr/local/bin`:

```bash
sudo mv terraform /usr/local/bin/
```

Verify the installation:

```bash
terraform --version
```

### Creating a service account

...

(Markdown truncated for brevity)
