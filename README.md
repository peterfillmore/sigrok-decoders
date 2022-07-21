<div id="top"></div>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/peterfillmore/sigrok_decoders">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">sigrok-decoders</h3>

  <p align="center">
    Various sigrok decoders under development
    <br />
    <a href="https://github.com/peterfillmore/sigrok_decoders"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/peterfillmore/sigrok_decoders">View Demo</a>
    ·
    <a href="https://github.com/peterfillmore/sigrok_decoders/issues">Report Bug</a>
    ·
    <a href="https://github.com/peterfillmore/sigrok_decoders/issues">Request Feature</a>
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
## About Sigrok-Decoders 
[![Product Name Screen Shot][product-screenshot]](https://example.com)

[![Product][pic12-screenshot]](https://github.com/peterfillmore/sigrokdecoders/images)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

To use a decoder do the following 

### Prerequisites

Install [https://sigrok.org/](Sigrok)

### Installation

Copy decoder into the libsigrokdecode/decoders folder, or set the SIGROKDECODE_DIR path
[https://sigrok.org/wiki/Protocol_decoder_HOWTO](Howto is here)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

###PIC12
####Viewing the signals
Name the clock signal as PGC, data signal as PGD. Target voltage and program voltage not yet implemented.

####dumping a read or write operations to binary
`SIGROKDECODE_DIR=./pic12 sigrok-cli -i ./traces/pic12f629_readprogram.sr -P pic12 -B pic12=readchip > test.bin`
`SIGROKDECODE_DIR=./pic12 sigrok-cli -i ./traces/pic12f629_writeprogram.sr -P pic12 -B pic12=loadchip > test.bin`

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [More PIC chips supported] Feature 1

See the [open issues](https://github.com/peterfillmore/sigrok_decoders/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

filsy

Project Link: [https://github.com/peterfillmore/sigrok_decoders](https://github.com/peterfillmore/sigrok_decoders)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/peterfillmore/sigrok_decoders.svg?style=for-the-badge
[contributors-url]: https://github.com/peterfillmore/sigrok_decoders/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/peterfillmore/sigrok_decoders.svg?style=for-the-badge
[forks-url]: https://github.com/peterfillmore/sigrok_decoders/network/members
[stars-shield]: https://img.shields.io/github/stars/peterfillmore/sigrok_decoders.svg?style=for-the-badge
[stars-url]: https://github.com/peterfillmore/sigrok_decoders/stargazers
[issues-shield]: https://img.shields.io/github/issues/peterfillmore/sigrok_decoders.svg?style=for-the-badge
[issues-url]: https://github.com/peterfillmore/sigrok_decoders/issues
[license-shield]: https://img.shields.io/github/license/peterfillmore/sigrok_decoders.svg?style=for-the-badge
[license-url]: https://github.com/peterfillmore/sigrok_decoders/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
