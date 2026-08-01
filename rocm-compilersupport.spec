# TheRock 7.14 Code Object Manager (comgr), built against system LLVM 23.
# Source is filtered amd/comgr from llvm-project @ therock-7.14.

%global comgr_maj_api_ver 3
%global comgr_full_api_ver %{comgr_maj_api_ver}.3.0

Name:		rocm-compilersupport
Version:	7.14.0
Release:	2
%{!?rocm_llvm_maj_ver:%global rocm_llvm_maj_ver 23}
Summary:	AMD ROCm LLVM-related services (Code Object Manager)
License:	Apache-2.0 WITH LLVM-exception
Group:		System/Libraries
URL:		https://github.com/ROCm/llvm-project
Source0:	amd_comgr-%{version}.tar.gz
Patch0:		0001-unordered-set-include.patch
Patch1:		0002-hotswap-amdgpu-parser.patch
Patch2:		0003-unbundle-offload-bundle.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
BuildRequires:	clang-devel >= %{rocm_llvm_maj_ver}
BuildRequires:	llvm-devel >= %{rocm_llvm_maj_ver}
BuildRequires:	lib64lld-devel >= %{rocm_llvm_maj_ver}
# comgr links static LLD (liblldELF.a); headers/cmake-only lib64lld-devel is not enough
BuildRequires:	lib64lldCommon-static-devel >= %{rocm_llvm_maj_ver}
BuildRequires:	lib64lldELF-static-devel >= %{rocm_llvm_maj_ver}
BuildRequires:	rocm-device-libs
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	python3


%description
Source package for ROCm compiler-support libraries. Currently ships
rocm-comgr (Code Object Manager / libamd_comgr), built from TheRock 7.14
sources against the system LLVM %{rocm_llvm_maj_ver} toolchain.

%package -n rocm-comgr
Summary:	AMD ROCm Code Object Manager
Provides:	comgr(major) = %{comgr_maj_api_ver}
Provides:	rocm-comgr = %{comgr_full_api_ver}-%{release}
Requires:	rocm-device-libs%{?_isa}
# Shared-lib deps on LLVM/clang are emitted by the ELF generator from
# NEEDED entries; explicit libllvm/libclang ISA Requires break on arches
# where those virtual Provides are missing or differently named.
Obsoletes:	rocm-comgr < %{EVRD}

%description -n rocm-comgr
libamd_comgr — create and inspect AMD code objects. Loaded at runtime by
CLR/HIP.

%package -n rocm-comgr-devel
Summary:	Development files for rocm-comgr
Requires:	rocm-comgr%{?_isa} = %{version}-%{release}
Requires:	rocm-device-libs = %{version}
Obsoletes:	rocm-comgr-devel < %{EVRD}

%description -n rocm-comgr-devel
Headers and CMake package for libamd_comgr.

%prep
%autosetup -n amd_comgr-%{version} -p1

# Configure in %%prep (%%cmake leaves cwd in build/)
%cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DBUILD_TESTING=OFF \
	-DCOMGR_BUILD_SHARED_LIBS=ON \
	-DCOMGR_DISABLE_SPIRV=ON \
	-DCOMGR_ENABLE_HOTSWAP_TRANSPILE=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%files -n rocm-comgr
%license LICENSE.txt
%doc README.md
%{_libdir}/libamd_comgr.so.%{comgr_full_api_ver}
%{_libdir}/libamd_comgr.so.%{comgr_maj_api_ver}
%exclude %{_docdir}/amd_comgr/LICENSE.txt
%exclude %{_docdir}/amd_comgr/README.md

%files -n rocm-comgr-devel
%{_includedir}/amd_comgr/
%{_libdir}/libamd_comgr.so
%{_libdir}/cmake/amd_comgr/
