# Blood-Bridge

Blood-Bridge is an innovative mobile application designed to bridge the critical gap between blood donors and recipients by utilizing advanced algorithms, specifically the bipartite maximal matching algorithm based on **Hall's Theorem**. The application aims to streamline the process of blood donation and distribution, ensuring swift and efficient assistance to those in need while optimizing the allocation of resources.

## Features

- **User Roles:** Blood-Bridge accommodates diverse user types, including donors, recipients, hospitals, and blood banks, each with specific functionalities tailored to their roles.
- **Status Setting:** Users can easily set their availability status as a donor, recipient, or inactive, providing real-time information for matching.
- **Comprehensive Insights:** Hospitals and blood banks gain access to comprehensive details of all matched donations within their facility, facilitating better management and coordination.
- **Matched Information:** Users receive pertinent information about matched donors or recipients along with the associated medical center, ensuring transparency and accountability.

## Blood-Bridge and Hall's Theorem

At the heart of Blood-Bridge's functionality lies **Hall's Theorem**, a mathematical principle that plays a pivotal role in the efficient matching of blood donors with recipients. Hall's Theorem provides a criterion for the existence of a perfect matching in bipartite graphs. In the context of Blood-Bridge:

- **Bipartite Graph:** Blood-Bridge models the relationships between donors and recipients as a bipartite graph, where donors form one set of vertices and recipients form the other set. An edge exists between a donor and recipient if they meet certain compatibility criteria such as blood type, location, and availability.

- **Matching Algorithm:** Hall's Theorem ensures that for every subset of donors, there exists a corresponding subset of recipients such that each donor is compatible with at least one recipient. This guarantees a maximal matching, maximizing the number of successful blood matches.

By leveraging Hall's Theorem, Blood-Bridge optimizes the blood donation process, allowing for timely and effective allocation of donated blood to those in urgent need, while also providing donors with a meaningful way to contribute to their community.

## Steps to Run the Project

To run the Blood-Bridge app, follow these steps:

1. **Install Flutter:** Set up Flutter on your PC by referring to the installation guide on the [Flutter website](https://flutter.dev/).
2. **Firebase Integration:** Create a Firebase project and connect it with the app. Sign up for a Firebase account, create a new project on the [Firebase website](https://firebase.google.com/), and follow the instructions to integrate it with Blood-Bridge.
3. **Matching Algorithm:** Execute MatchingScript.py after providing the correct path of the Firebase credential file. Update the script with the credential file path, and run the script to initiate the donor-recipient matching process.

---

This README provides a comprehensive overview of the Blood-Bridge application, its underlying algorithm based on Hall's Theorem, and step-by-step instructions for running the project. Customize and enhance the content further to suit your project's unique attributes and goals.