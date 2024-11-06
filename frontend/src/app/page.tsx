import { Button } from "@components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@components/ui/card";

const HomePage = async () => {
  // print env
  const endpoint: string = process.env.NEXT_PUBLIC_API_ENDPOINT as string;

  const data = await fetch(endpoint);
  const msg: { hello: string } = await data.json();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Title</CardTitle>
      </CardHeader>

      <CardContent>
        <p>{endpoint}</p>
        <p>Message from backend: {msg.hello}</p>
      </CardContent>

      <CardFooter className="flex justify-between">
        <Button variant="outline">Outline variant</Button>
        <Button>Default variant</Button>
      </CardFooter>
    </Card>
  );
};

export default HomePage;
