<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/patdaburu/gardenio">
    <img src="../../../../img/logo.svg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Ubuntu 20.04</h3>

  <p align="center">
    Focal Fossa
    <br />
    <a href="https://github.com/patdaburu/gardenio"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/patdaburu/gardenio/issues">Report Bug</a>
    ·
    <a href="https://github.com/patdaburu/gardenio/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[GDAL](https://gdal.org/) for [gardenio](https://github.com/patdaburu/gardenio) builds a [docker](https://www.docker.com/) container with GDAL installed and ready to go.  You can use this as a base for application containers that require GDAL.

What's more: When you run this container you can download an archive that you can use to run GDAL in your development environment or elsewhere.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [docker](https://www.docker.com/)
* [just](https://github.com/casey/just)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

You'll need a few tools, including:

* [docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)
* [just](https://docs.docker.com/compose/install/)
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)



### Installation

1. Clone this repository.

```sh
git clone https://github.com/Geo-Comm/dockers
```

2. `cd` to the directory containing this `README`.


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

You can do most of the things you'll want to do with [just](https://github.com/casey/just) recipes.

```sh
$ just --list
Available recipes:
    build # Build the container image.
    clean # Clean up dangling images.
    login # Shell into the container.
    run   # Run the container.
```

1. Build the container.

```sh
just build
```

2. Run the container.

```sh
just run
```

### Using the Binaries

If you want to get the binaries to use in your environment, here's how to do it.

1. Download the binaries.  You can see what's available at `http:localhost:8088`.

2. Extract the archive.

3. Set up your environment variables to point to the extract location.

```sh
export GDAL_BASE=/path/to/gdal
export PATH=$PATH:$GDAL_BASE/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$GDAL_BASE/lib
export GDAL_DATA=$GDAL_BASE/share/gdal
```



<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

We're still reviewing licenses.  Stay tuned.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/patdaburu/gardenio](https://github.com/github_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/patdaburu/gardenio/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
