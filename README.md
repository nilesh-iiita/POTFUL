# :stew: POTFUL
POTFUL Plant cO-expression Transcription Factor regULators


![](POTFUL_Animate/POTFUL.gif)


## Setup
::::{grid}

:::{grid-item-card} OS!
Windows 11 (5.10.102.1-microsoft-standard-WSL2), and Fedora 36.
:::

::::


::::{grid}
:gutter: 4

:::{grid-item-card} RAM!
16 GB 
:::

:::{grid-item-card} SDD!
256 GB 
:::

:::{grid-item-card} CPU!
Intel i7
:::

:::{grid-item-card} Conda!
v4.12.0
:::
::::

A major requirement for `POTFUL` is `RUST`. The user must first install RUST on the OS of their choice.

## Install Rust

````{tab-set}
```{tab-item} Linux, WSL2 and mac OS
    curl https://sh.rustup.rs -sSf | sh
```

```{tab-item} Windows 11/10
    run [vs_BuildTools.exe](https://aka.ms/vs/17/release/vs_BuildTools.exe) # `Microsoft C++ Build Tools`
    run rustup-init.exe[https://win.rustup.rs/]
```
````

```{seealso}
You can learn a lot more at [The Cargo Book](https://doc.rust-lang.org/cargo/getting-started/installation.html). 
```
{cite}`RUST` 

## Create conda environment

````{tab-set}
```{tab-item} Fedora (36<) and Ubuntu (22<) and WSL2
[POTFUL.yml](https://github.com/nilesh-iiita/POTFUL/blob/main/POTFUL.yml)

    conda env create -n POTFUL --file POTFUL.yml
```

```{tab-item} Mac OS
[POTFUL_macPy39.yml](https://github.com/nilesh-iiita/POTFUL/blob/main/POTFUL_macPy39.yml)

    conda env create -n POTFUL --file POTFUL_macPy39.yml
```

```{tab-item} Windows 11/10
[POTFUL_WinPy39.yml](https://github.com/nilesh-iiita/POTFUL/blob/main/POTFUL_WinPy39.yml)

    conda env create -n POTFUL --file POTFUL_WinPy39.yml
```
````


## Clone git repository

Fork the [POTFUL](https://github.com/nilesh-iiita/POTFUL) git repository and clone or download.

    git clone https://github.com/<User Name>/POTFUL.git
