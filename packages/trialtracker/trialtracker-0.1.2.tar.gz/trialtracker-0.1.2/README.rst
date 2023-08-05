.. raw:: html

   <!-- PROJECT SHIELDS -->

.. raw:: html

   <!--
   *** I'm using markdown "reference style" links for readability.
   *** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
   *** See the bottom of this document for the declaration of the reference variables
   *** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
   *** https://www.markdownguide.org/basic-syntax/#reference-style-links

   reference file here https://gitlab.unige.ch/Joakim.Tutt/Best-README-Template/-/tree/master
   -->

.. raw:: html

   <!-- [![Contributors][contributors-shield]][contributors-url]
   [![Forks][forks-shield]][forks-url]
   [![Stargazers][stars-shield]][stars-url]
   [![Issues][issues-shield]][issues-url]
   [![MIT License][license-shield]][license-url]
   [![LinkedIn][linkedin-shield]][linkedin-url] -->

.. raw:: html

   <!-- PROJECT LOGO -->

.. raw:: html

   <p align="center">

.. raw:: html

   <!--   <a href="https://github.com/othneildrew/Best-README-Template">
       <img src="images/logo.png" alt="Logo" width="80" height="80">
     </a>
    -->

.. raw:: html

   <h3 align="center">

Trial Tracker

.. raw:: html

   </h3>

.. raw:: html

   <p align="center">

Improving cancer research with data!

.. raw:: html

   </p>

.. raw:: html

   </p>

.. raw:: html

   <!-- TABLE OF CONTENTS -->

Table of Contents
-----------------

-  `What is it? <#what-is-it>`__
-  `Main Features <#main-features>`__
-  `Impact <#impact>`__
-  `Built With <#built-with>`__
-  `Getting Started <#getting-started>`__

   -  `Prerequisites <#prerequisites>`__
   -  `Installation <#installation>`__

-  `Usage <#usage>`__
-  `Roadmap <#roadmap>`__
-  `Contributing <#contributing>`__
-  `License <#license>`__
-  `Contact <#contact>`__
-  `Acknowledgements <#acknowledgements>`__

.. raw:: html

   <!-- What is it -->

What is it?
-----------

trialtracker is a Python package that provides methods to easily
extract, transform, and download clinical trial data. It aims to create
standardized data infrastructure for clinical trial digitalization,
focusing on structured representation of clinical trial protocols.

.. raw:: html

   <!-- Main Features -->

Main Features
-------------

Here are some of the things trialtracker allows you to do:

- Download pre-curated clinical trial and clinical trial eligibility
criteria datasets - Easily query data from clinicaltrials.gov - Apply
state-of-the-art natural language processing methods to extract useful
information from raw clinicaltrials.gov data - Data visualizations and
analysis of clinical trial data

The current version of the package is primarily focused on cancer
trials, which are an important area for clinical development. Improved
data infrastructure is especially helpful in this area given the
complexity of the disease and treatments.

.. raw:: html

   <!-- Impact -->

Impact
------

.. raw:: html

   <!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

Cancer is one of the leading causes of death worldwide. The way we test
and approve new treatments is through clinical trials. But 97% of cancer
trials fail, driven by inability to recruit enough patients. And yet
many patients are routinely excluded from trials, including minority
groups who are most affected by the disease.

The key to solving these problems is in changing how we design trials,
recruit patients, and report on results. Regulatory requirements for
clinical trial registration became required in 2017, making
semi-structured trial protocol data available on clinicaltrials.gov.
Today, this is not being systematically used in trial design, patient
recruitment, or reporting decisions in Oncology. This project aims to
unlock the value of clinical trial data to help accelerate cancer
research and improve the lives of cancer patients.

.. raw:: html

   <!-- A few goals of this project:    
   <br /> - Explore clinical trial data from clinicaltrials.gov
       <br /> - Develop a method to extract structured core eligibility criteria for cancer trials (extending work  
       <a href="https://pubmed.ncbi.nlm.nih.gov/30753493/">here</a>  and 
       <a href="https://arxiv.org/abs/2006.07296">here</a>)
       <br /> - Combine extracted criteria with real-world oncology data to evaluate the impact of eligibility criteria on trial racial diversity (extending work 
       <a href="https://www.nature.com/articles/s41586-021-03430-5">here</a> by incorporating race data)
       <br /> - Generate a diversity rating for each clinical trial -->

Built With
~~~~~~~~~~

Technologies and methods used to build this project! \*
`Python <https://www.python.org/>`__ \* `Golang <https://go.dev/>`__ \*
`Named Entity Recognition and Named Entity
Linking <https://arxiv.org/abs/2006.07296>`__

.. raw:: html

   <!-- GETTING STARTED -->

Getting Started
---------------

To get a local copy up and running follow the steps below.

Prerequisites
~~~~~~~~~~~~~

Get up and running with conda. Given the many dependencies of this
project, we use conda as a package/environment manager to make sure
we’re running things in the same environment and that nothing breaks :)

Installation
~~~~~~~~~~~~

1. Clone the repo

.. code:: sh

   git clone https://github.com/zfx0726/trialtracker.git

2. Navigate into the trialtracker project directory and recreate the
   conda environment.

.. code:: sh

   conda env create --file=trialtrackerenv_py36.yaml

3. Activate conda python environment

.. code:: sh

   conda activate trialtrackerenv_py36

Running eligibility criteria extraction with FB Clinical Trial Parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download the MeSH vocabulary, from root directory:

.. code:: sh

   ./extract/src/github.com/facebookresearch/Clinical-Trial-Parser/script/mesh.sh

2. Navigate into the trialtracker project directory and recreate the
   conda environment.

Running eligibility criteria extraction with pyMeSHSim
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download and extract MetaMap as per:

.. code:: https://pymeshsim.readthedocs.io/en/latest/install.html

2. 

.. raw:: html

   <!-- ROADMAP -->

.. raw:: html

   <!-- ## Roadmap

   See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a list of proposed features (and known issues).
    -->

.. raw:: html

   <!-- CONTRIBUTING -->

Contributing
------------

Contributions are what make the open source community such an amazing
place to be learn, inspire, and create. Any contributions you make are
**greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch
   (``git checkout -b feature/AmazingFeature``)
3. Commit your Changes (``git commit -m 'Add some AmazingFeature'``)
4. Push to the Branch (``git push origin feature/AmazingFeature``)
5. Open a Pull Request

.. raw:: html

   <!-- LICENSE -->

License
-------

Distributed under the MIT License. See \ ``LICENSE``\  for more
information.

.. raw:: html

   <!-- CONTACT -->

Contact
-------

.. raw:: html

   <!-- Forrest Xiao - [@your_twitter](https://twitter.com/your_username) - email@example.com -->

Forrest Xiao - zfx0726@gmail.com

.. raw:: html

   <!-- ACKNOWLEDGEMENTS -->

.. raw:: html

   <!-- ## Acknowledgements
   * [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
   * [Img Shields](https://shields.io)
   * [Choose an Open Source License](https://choosealicense.com)
   * [GitHub Pages](https://pages.github.com)
   * [Animate.css](https://daneden.github.io/animate.css)
   * [Loaders.css](https://connoratherton.com/loaders)
   * [Slick Carousel](https://kenwheeler.github.io/slick)
   * [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
   * [Sticky Kit](http://leafo.net/sticky-kit)
   * [JVectorMap](http://jvectormap.com)
   * [Font Awesome](https://fontawesome.com)
    -->

.. raw:: html

   <!-- MARKDOWN LINKS & IMAGES -->

.. raw:: html

   <!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

.. raw:: html

   <!-- [contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
   [contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
   [forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
   [forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
   [stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
   [stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
   [issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
   [issues-url]: https://github.com/othneildrew/Best-README-Template/issues
   [license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
   [license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
   [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
   [linkedin-url]: https://linkedin.com/in/othneildrew
   [product-screenshot]: images/screenshot.png -->
